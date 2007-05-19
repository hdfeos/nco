#ifndef INC_ncoParserTokenTypes_hpp_
#define INC_ncoParserTokenTypes_hpp_

/* $ANTLR 2.7.6 (20070220): "ncoGrammer.g" -> "ncoParserTokenTypes.hpp"$ */

#ifndef CUSTOM_API
# define CUSTOM_API
#endif

#ifdef __cplusplus
struct CUSTOM_API ncoParserTokenTypes {
#endif
	enum {
		EOF_ = 1,
		NULL_NODE = 4,
		BLOCK = 5,
		ARG_LIST = 6,
		DMN_LIST = 7,
		DMN_ARG_LIST = 8,
		LMT_LIST = 9,
		VALUE_LIST = 10,
		FUNC_ARG = 11,
		LMT = 12,
		EXPR = 13,
		POST_INC = 14,
		POST_DEC = 15,
		SQR2 = 16,
		PROP = 17,
		SEMI = 18,
		LCURL = 19,
		RCURL = 20,
		IF = 21,
		LPAREN = 22,
		RPAREN = 23,
		ELSE = 24,
		VAR_ID = 25,
		ATT_ID = 26,
		DEFDIM = 27,
		NSTRING = 28,
		COMMA = 29,
		DIM_ID = 30,
		DIM_MTD_ID = 31,
		FUNC = 32,
		PAVG = 33,
		PAVGSQR = 34,
		PMAX = 35,
		PMIN = 36,
		PRMS = 37,
		PRMSSDN = 38,
		PSQR = 39,
		ARVG = 40,
		PTTL = 41,
		DOT = 42,
		PSIZE = 43,
		PTYPE = 44,
		PNDIMS = 45,
		INC = 46,
		DEC = 47,
		LNOT = 48,
		PLUS = 49,
		MINUS = 50,
		TIMES = 51,
		CARET = 52,
		DIVIDE = 53,
		MOD = 54,
		LTHAN = 55,
		GTHAN = 56,
		GEQ = 57,
		LEQ = 58,
		EQ = 59,
		NEQ = 60,
		LAND = 61,
		LOR = 62,
		QUESTION = 63,
		COLON = 64,
		ASSIGN = 65,
		PLUS_ASSIGN = 66,
		MINUS_ASSIGN = 67,
		TIMES_ASSIGN = 68,
		DIVIDE_ASSIGN = 69,
		LSQUARE = 70,
		RSQUARE = 71,
		FLOAT = 72,
		DOUBLE = 73,
		INT = 74,
		SHORT = 75,
		USHORT = 76,
		UINT = 77,
		BYTE = 78,
		DIM_ID_SIZE = 79,
		NRootAST = 80,
		SHIFTL = 81,
		SHIFTR = 82,
		PSQRAVG = 83,
		QUOTE = 84,
		DGT = 85,
		LPH = 86,
		LPHDGT = 87,
		XPN = 88,
		BLASTOUT = 89,
		UNUSED_OPS = 90,
		Whitespace = 91,
		CXX_COMMENT = 92,
		C_COMMENT = 93,
		NUMBER_DOT = 94,
		NUMBER = 95,
		VAR_ATT = 96,
		VAR_ATT_QT = 97,
		DIM_VAL = 98,
		LMT_DMN = 99,
		NULL_TREE_LOOKAHEAD = 3
	};
#ifdef __cplusplus
};
#endif
#endif /*INC_ncoParserTokenTypes_hpp_*/
