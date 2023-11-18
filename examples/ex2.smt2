(declare-const x Real)
(assert (> x 1.0))
(assert (not (> x 0.0)))
(check-sat)
