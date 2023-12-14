short nondet_short();

short short_to_bool(short val) {
    if (val == 0) {
        return 0;
    } else {
        return 1;
    }
}

short short_to_range(short val) {
    if (val < 0) {
        return 0;
    }
    if (val>10) {
        return 10;
    }
}

short credit1(short group, short score) {
  if (group == 0) {
    return 0;
  } else {
    return 1;
  }
}

short credit3(short group, short score) {
  if (group >= 6) {
    return (score >= 8) ? 1 : 0;
  } else {
    return (score >= 6) ? 1 : 0;
  }
}

short credit2(short group, short score) {
  if (score < 8) {
    return 0;
  } else {
    return 1;
  }
}

void testfun1(short score, short decision) {
    __counterSharp_assume(decision==0 || decision==1);
    __counterSharp_assume(1 <= score && score <= 10);
    short age = nondet_short();
    age = short_to_range(age);
    short result = credit1(age, score);
    short result_bool = short_to_bool(result);
    short decision_result = short_to_bool(decision);
    __counterSharp_assert(result_bool != decision_result);
}

void testfun3(short score, short decision) {
    __counterSharp_assume(decision==0 || decision==1);
    __counterSharp_assume(1 <= score && score <= 10);
    short age = nondet_short();
    age = short_to_range(age);
    short result = credit3(age, score);
    short result_bool = short_to_bool(result);
    short decision_result = short_to_bool(decision);
    __counterSharp_assert(result_bool != decision_result);
}

short non_uniform(short score) {
    if (score <= 20) {
        return 1; // 20%
    } else if (score <= 25) {
        return 2; // 5%
    } else if (score <= 30) {
        return 3; // 5%
    } else if (score <= 35) {
        return 4; // 5%
    } else if (score <= 45) {
        return 5; // 10%
    } else if (score <= 60) {
        return 6; // 15%
    } else if (score <= 75) {
        return 7; // 15%
    } else if (score <= 80) {
        return 8; // 5%
    } else if (score <= 85) {
        return 9; // 5%
    } else {
        return 10; // 15%
    }
}

void testfun3NonUniform(short score, short decision) {
    __counterSharp_assume(decision==0 || decision==1);
    __counterSharp_assume(1 <= score && score <= 100);
    score = non_uniform(score);
    short age = nondet_short();
    age = short_to_range(age);
    short result = credit3(age, score);
    short result_bool = short_to_bool(result);
    short decision_result = short_to_bool(decision);
    __counterSharp_assert(result_bool != decision_result);
}

void testfun2(short score, short decision) {
    __counterSharp_assume(decision==0 || decision==1);
    __counterSharp_assume(1 <= score && score <= 10);
    short age = nondet_short();
    age = short_to_range(age);
    short result = credit2(age, score);
    short result_bool = short_to_bool(result);
    short decision_result = short_to_bool(decision);
    __counterSharp_assert(result_bool != decision_result);
}