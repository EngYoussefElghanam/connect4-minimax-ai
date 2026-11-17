# Design decisions to settle before coding (put the final answers in the report)

- [ ] Board size (min width 7, height 6). Fixed in `config.py`.
- [ ] How are connected-fours counted? Plan: every window of 4 consecutive discs counts,
      so a line of 5 = 2 fours. (Tests assume this.)
- [ ] Game does NOT stop at the first four; it continues until the board is full,
      winner = greater number of fours. Terminal utility = final score difference.
- [ ] Who moves first? (Plan: human, configurable.)
- [ ] Move ordering in alpha-beta (left-to-right vs centre-first). Affects nodes expanded.
- [ ] Tie-break between equal-valued moves.
- [ ] K per difficulty (EASY / MEDIUM / HARD) and allowed custom K range.
- [ ] Heuristic sign convention: positive = good for the COMPUTER, negative = good for the HUMAN.
