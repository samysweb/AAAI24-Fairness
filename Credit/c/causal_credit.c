short nondet_short();

short to_group(short val) {
    if (val <= 0) {
        return 5;
    // } else if (val >= 9) {
    //     return 9;
    } else {
        return 6;
    }
}

short getCredit(short g, short c) {
    if (g >= 6 && c >= 8) {
        return 1;
    } else if (g < 6 && c >= 6) {
        return 1;
    } else {
        return 0;
    }
}

short getCredit2(short g, short c) {
    if (c >= 8) {
        return 1;
    } else {
        return 0;
    }
}
short causal_c1(short g, short u1, short u2, short u3) {
    int income = u1;
    int zipCodeRank = (g >= 6) ? u2 : u3;
    return income + zipCodeRank;
}
void testfun1(short u1, short u2, short u3, short d) {
    __counterSharp_assume(0 <= d && d <= 1);
    __counterSharp_assume(0 <= u1 && u1 <= 9);
    __counterSharp_assume(-1 <= u2 && u2 <= 5);
    __counterSharp_assume(-3 <= u3 && u3 <= 3);
    short g_short = nondet_short();
    short g = to_group(g_short);
    short score = causal_c1(g, u1, u2, u3);
    short r = getCredit(g, score);
    __counterSharp_assert(r != d);
}
// Fairness Spread: 22.9%

void testfun2(short u1, short u2, short u3, short d) {
    __counterSharp_assume(0 <= d && d <= 1);
    __counterSharp_assume(0 <= u1 && u1 <= 9);
    __counterSharp_assume(-1 <= u2 && u2 <= 5);
    __counterSharp_assume(-3 <= u3 && u3 <= 3);
    short g_short = nondet_short();
    short g = to_group(g_short);
    short score = causal_c1(g, u1, u2, u3);
    short r = getCredit2(g, score);
    __counterSharp_assert(r != d);
}
// Fairness Spread: 26.7%

void testfun1path(short u0, short u1, short u2, short u3, short zip_path, short d) {
    __counterSharp_assume(0 <= d && d <= 1);
    __counterSharp_assume(u0 == 5 || u0 == 6);
    __counterSharp_assume(0 <= u1 && u1 <= 9);
    __counterSharp_assume(-1 <= u2 && u2 <= 5);
    __counterSharp_assume(-3 <= u3 && u3 <= 3);
    __counterSharp_assume(u0 == 5 && (-3 <= zip_path && zip_path <= 3) || u0 == 6 && (-1 <= zip_path && zip_path <= 5));
    //__counterSharp_assume(-3 <= zip_path && zip_path <= 5);
    short g_short = nondet_short();
    short g = to_group(g_short);
    short score = causal_c1(g, u1, zip_path, zip_path);
    short r = getCredit(g, score);
    __counterSharp_assert(r != d);
}
// Fairness Spread: 19,2%

void testfun2path(short u0, short u1, short u2, short u3, short zip_path, short d) {
    __counterSharp_assume(0 <= d && d <= 1);
    __counterSharp_assume(u0 == 5 || u0 == 6);
    __counterSharp_assume(0 <= u1 && u1 <= 9);
    __counterSharp_assume(-1 <= u2 && u2 <= 5);
    __counterSharp_assume(-3 <= u3 && u3 <= 3);
    __counterSharp_assume(u0 == 5 && (-3 <= zip_path && zip_path <= 3) || u0 == 6 && (-1 <= zip_path && zip_path <= 5));
    short g_short = nondet_short();
    short g = to_group(g_short);
    short score = causal_c1(g, u1, zip_path, zip_path);
    short r = getCredit2(g, score);
    __counterSharp_assert(r != d);
}
// Fairness Spread: 0%

void testfun1count(short u1, short u2, short u3, short d) {
    __counterSharp_assume(0 <= d && d <= 1);
    __counterSharp_assume(0 <= u1 && u1 <= 9);
    __counterSharp_assume(-1 <= u2 && u2 <= 5);
    __counterSharp_assume(-3 <= u3 && u3 <= 3);
    short g_short = nondet_short();
    short g = 6;
    short score = causal_c1(g, u1, u2, u3);
    short r = getCredit(g, score);
    __counterSharp_assert(r == 1);
}