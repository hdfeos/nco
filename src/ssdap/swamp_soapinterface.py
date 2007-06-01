# $Header: /data/zender/nco_20150216/nco/src/ssdap/swamp_soapinterface.py,v 1.1 2007-06-01 00:56:14 wangd Exp $
# Copyright (c) 2007 Daniel L. Wang
from swamp_common import *
from swamp_config import Config 
import cPickle as pickle
import logging
import os
import SOAPpy
import threading 
import twisted.web.soap as tSoap
import twisted.web.resource as tResource
import twisted.web.server as tServer
import twisted.web.static as tStatic

log = logging.getLogger("SWAMP")

class LaunchThread(threading.Thread):
    def __init__(self, swampint, script, updateFunc):
        threading.Thread.__init__(self) 
        self.script = script
        self.swampInterface = swampint
        self.updateFunc = updateFunc
        pass
    def run(self):
        self.updateFunc(self) # put myself as placeholder
        log.info("Starting workflow execution")
        task = self.swampInterface.submit(self.script)
        log.info("Finished workflow execution got id=%s" % task.taskId())
        # should update with an object that can be used to
        #query for task state.
        self.updateFunc(task) # update with real object

class StandardJobManager:
    """StandardJobManager manages submitted tasks dispatched by this system.
    """
    def __init__(self, cfgName=None):
        if cfgName:
            self.config = Config(cfgName)
        else:
            self.config = Config()
        self.config.read()

        le = LocalExecutor.newInstance(self.config)
        self.swampInterface = SwampInterface(self.config, le)

        self.token = 0
        self.tokenLock = threading.Lock()
        self.jobs = {}
        pass
    def reset(self):
        # Clean up trash from before:
        # - For now, don't worry about checking jobs still in progress
        # - Delete all the physical files we allocated in the file mapper
        log.info("Reset requested--disabled")
        #self.fileMapper.cleanPhysicals()
        log.info("Reset finish")
        
    def slaveExec(self, pickledCommand):
        log.info("shouldn't be here...")
        return 0
        cf = CommandFactory(self.config)
        p = cf.unpickleCommand(pickledCommand)
        self.tokenLock.acquire()
        self.token += 1
        token = self.token + 0
        self.tokenLock.release()
        log.info("received cmd: %s %d token=%d outs=%s"
                 % (p.cmd, p.referenceLineNum, token, str(p.outputs)))
        self._threadedLaunch(p, token)
        return token

    def newScriptedFlow(self, script):
        self.tokenLock.acquire()
        self.token += 1
        token = self.token + 0
        self.tokenLock.release()
        log.info("Received new workflow (%d) {%s}" % (token, script))
        self._threadedLaunch(script, token)
        log.debug("return from thread launch (%d)" % (token))
        return token

    def pyInterface(self, cmdline):
        """pyInterface(cmdline) : runs an arbitrary python commmand
        line and returns its results.  This is a huge security hole that
        should be disabled for live systems.

        It's very handy during development, though."""
        try:
            return str(eval(cmdline))
        except Exception, e:
            import traceback, sys
            tb_list = traceback.format_exception(*sys.exc_info())
            return "".join(tb_list)
        
    def _updateToken(self, token, etoken):
        self.jobs[token] = etoken
        
    def _threadedLaunch(self, script, token):
        launchthread = LaunchThread(self.swampInterface, script,
                                    lambda x: self._updateToken(token, x))
        launchthread.start()
        log.debug("started launch")
        #launchthread.join()
        return 

    def pollState(self, token):
        if token not in self.jobs:
            time.sleep(0.2) # possible race
            if token not in self.jobs:
                log.warning("token not ready after waiting.")
                return None
        if isinstance(self.jobs[token], threading.Thread):
            return None # token not even ready, arg fetch.
        #log.debug("trying exec poll" + str(self.jobs) + str(token))
        # for now, if the interface is there,
        #things are complete/okay.
        if isinstance(self.jobs[token], SwampTask):
            return 0
        else:
            return None

    def pollStateMany(self, tokenList):
        return map(self.pollState, tokenList)

    def actualToPub(self, f):
        relative = f.split(self.config.execScratchPath + os.sep, 1)
        if len(relative) < 2:
            relative = f.split(self.config.execBulkPath + os.sep, 1)
            return self.bulkExportPref + relative[1]
        else:
            return self.scratchExportPref + relative[1]
    
    def pollOutputs(self, token):
        assert token in self.jobs
        outs = self.jobs[token].realOuts
        # FIXME: need to figure out a good way to give stuff back to the user.
        return outs

    def discardFile(self, f):
        log.debug("Discarding "+str(f))
        self.fileMapper.discardLogical(f)

    def discardFiles(self, fList):
        log.debug("Bulk discard "+str(fList))
        #for f in fList:
        for i in range(len(fList)):
            self.fileMapper.discardLogical(fList[i])
        #map(self.fileMapper.discardLogical, fList)

    def startSlaveServer(self):
        #SOAPpy.Config.debug =1
    
        server = SOAPpy.SOAPServer(("localhost", self.config.slavePort))
        server.registerFunction(self.slaveExec)
        server.registerFunction(self.pollState)
        server.registerFunction(self.pollStateMany)
        server.registerFunction(self.pollOutputs)
        server.registerFunction(self.reset)
        server.registerFunction(self.discardFile)
        server.registerFunction(self.discardFiles)
        server.serve_forever()
        pass

    def startTwistedServer(self):
        from twisted.internet import reactor
        root = tResource.Resource()
        pubRes = tStatic.File(self.config.execResultPath)
        tStatic.loadMimeTypes() # load from /etc/mime.types
        root.putChild(self.config.serverFilePath, pubRes)
        root.putChild(self.config.serverPath, TwistedSoapSwampInterface(self))
        reactor.listenTCP(self.config.serverPort, tServer.Site(root))
        log.debug("starting swamp SOAP ")
        reactor.run()
        pass
    pass # end class StandardJobManager

class ScriptContext:
    """Contains objects necessary to manage *ONE* script's running context"""
    def __init__(self, config):
        self.config = config

        self.sched = Scheduler(config, None) # build schedule without executor.
        self.commandFactory = CommandFactory(config)
        self.parser = Parser()
        self.taskId = self.sched.makeTaskId()
        pass
    def addScript(self, script):
        self.script = script
        
        pass

    def addTree(self, tree):
        raise StandardError("Tree accepting not implemented")
    

    def id(self):
        return self.taskId
    
    def run(self, context):
        # actually, want to request resources from the system,
        # then build control structures, and then execute.
        self.sched.executeParallelAll(self.remote)
        pass
    pass

class TwistedSoapSwampInterface(tSoap.SOAPPublisher):
    def __init__(self, jobManager):
        self.jobManager = jobManager
    def soap_reset(self):
        return self.jobManager.reset()
    def soap_newScriptedFlow(self, script):
        return self.jobManager.newScriptedFlow(script)
    def soap_pollState(self, token):
        return self.jobManager.pollState(token)
    def soap_pollOutputs(self, token):
        return self.jobManager.pollOutputs(token)
    def soap_pyInterface(self, cmdline): # huge security hole for debugging
        return self.jobManager.pyInterface(cmdline)


class SwampExtInterface:
    
    def submitScript(self, script):
        """spawn a thread to get things started, assign a task id,
        and return it."""
        sc = ScriptContext(self.config)
        sc.addScript(script)
        taskid = sc.id()
        self.forkOff(sc)
        return taskid

    def submitTree(self, parsedFlow):
        """accept an already parsed, disambiguated, DAG workflow,
        and execute it"""
        sc = ScriptContext(self.config)
        sc.addTree(script)
        taskid = sc.id()
        self.forkOff(sc)
        return taskid

    
    def retrieveResults(self, taskid):
        """return a list of filenames and urls"""
        pass
    def discard(self, taskid):
        """free all resources associated with this taskid"""
        # this probably kills a job in progress.
        pass
        
        pass
    pass # end class SwampExtInterface
    

def selfTest():
    pass

def clientTest():
    import SOAPpy
    serverConf = Config("swampsoap.conf")
    serverConf.read()
    server = SOAPpy.SOAPProxy("http://localhost:%d/%s"
                              %(serverConf.serverPort,
                                serverConf.serverPath))
    if len(sys.argv) > 2:
        import readline
        while True:
            print server.pyInterface(raw_input())
    else:
        server.reset()
        tok = server.newScriptedFlow("""
ncwa -a time camsom1pdf/camsom1pdf_10_clm.nc timeavg.nc
ncwa -a lon timeavg.nc timelonavg.nc
    """)
        print "submitted, got token: ", tok
        while True:
            ret = server.pollState(tok)
            if ret is not None:
                print "finish, code ", ret
                break
            time.sleep(1)
        print "actual outs are at", server.pollOutputs(tok)


def main():
    selfTest()
    if (len(sys.argv) > 1) and (sys.argv[1] == "--"):
        clientTest()
    else:
        jm = StandardJobManager("swampsoap.conf")
        #jm.startSlaveServer()
        jm.startTwistedServer()

if __name__ == '__main__':
    main()

