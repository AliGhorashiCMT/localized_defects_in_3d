(define-param rvecs (list (vector3 1 0 0) (vector3 0 1 0) (vector3 0 0 1)))
(define-param epsin 16.0)
(define-param epsout 1.0)
(define-param isoval 1.1)

(define twopi 6.28318530718)
(set! num-bands 10)
(set! resolution 32)
(define a (/ 1 2))
(define basissize (/ (sqrt 3) 2))
(define gamma (vector3 0 0 0))
(define H (vector3 -0.5 0.5 0.5))
(define N (vector3 0 0.5 0))
(define P (vector3 0.25 0.25 0.25))

(set! geometry-lattice (make lattice (size 1 1 1)
            (basis1 (vector3 (* a -1) a a)) (basis2 (vector3 a (* a -1)  a)) (basis3 (vector3 a a (* a -1)))
            (basis-size basissize basissize basissize)))


(define (epsxyz x y z)
     (+ (* (sin x) (cos y))  (* (sin y) (cos z)) (* (sin z) (cos x))) ; try to replace the places where it goes below vacuum
)

(define (singlegyroid v)
	(cond ((> (epsxyz (* twopi (vector3-x v)) (* twopi (vector3-y v))  (* twopi (vector3-z v))) isoval) epsin)
	(else epsout))
) 

(define (doublegyroid v)
        (cond ((> (abs (epsxyz (* twopi (vector3-x v)) (* twopi (vector3-y v))  (* twopi (vector3-z v)))) isoval) epsin)
        (else epsout))
)

(define (doublegyroid-primitive v)
	(doublegyroid (vector3 (* (+ (* (vector3-x v) -1) (vector3-y v) (vector3-z v)) a) 
	(* (+ (* (vector3-y v) -1) (vector3-x v) (vector3-z v)) a)
	(* (+ (* (vector3-z v) -1) (vector3-y v) (vector3-x v)) a))) 
)

(set! default-material (make material-function (epsilon-func doublegyroid-primitive)))
;(set! default-material (make material-function (epsilon-func singlegyroid)))

(set! k-points (list N gamma H P N))
(set! k-points (interpolate 100 k-points))

(run)


