(declare-fun f (Real) Real)
(declare-const b Real)
(assert (= (f b) 0))
(declare-const a Real)
(assert (= (f (* 2 a)) 0))
(assert (distinct (* 2 a) b))
(assert (forall ((x Real)) (= (f x) (+ (+ (^ x 2) (* a x)) b))))
(assert (not (= (+ a b) (- 1))))
(check-sat)
