package org;

class Sample1 {
    /*@ determines \result \by score;
      @*/
    public boolean credit1(int group, int score) {
        if (group == 0) {
            return false;
        } else {
            return true;
        }
    }

    /*@ determines \result \by score;
      @*/
    public boolean credit2(int group, int score) {
        if (score < 8) {
            return false;
        } else {
            return true;
        }
    }

    /*@ requires !(group >= 6 && score >= 6 && score < 8);
      @ determines \result \by score;
      @*/
    public boolean credit3(int group, int score) {
        if (group >= 6) {
            return (score >= 8);
        } else {
            return (score >= 6);
        }
    }
}