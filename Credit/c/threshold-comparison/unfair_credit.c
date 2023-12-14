short short_to_range(short val) {
    if (val < 0) {
        return 0;
    }
    if (val>2) {
        return 2;
    }
}

#define T 10
// 0 => 10 => 0.33 => 0.0
// 1 => 12 => 0.4 => 0.2
// 2 => 14 => 0.47 => 0.4
// 3 => 16 => 0.53 => 0.6
// 4 => 18 => 0.6 => 0.8
// 5 => 20 => 0.67 => 1.0
// 6 => 18 => 0.6 => 0.8
// 7 => 16 => 0.53 => 0.6
// 8 => 14 => 0.47 => 0.4
// 9 => 12 => 0.4 => 0.2
// 10 => 10 => 0.33 => 0.0



short credit(short gender, short amount) {
    if(gender==0) {
        return (amount <= T) ? 1 : 0;
    } else {
        return (amount > (10-T)) ? 1 : 0;
    }
}

void testfun(short amount, short decision) {
    __counterSharp_assume(decision==0 || decision==1);
    __counterSharp_assume(1 <= amount && amount <= 10);
    short gender = nondet_short();
    gender = short_to_range(gender);
    short result = credit(gender, amount);
    __counterSharp_assert(result != decision);
}