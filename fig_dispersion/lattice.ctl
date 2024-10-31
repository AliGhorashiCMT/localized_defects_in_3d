(define-param rvecs (list (vector3 1 0 0) (vector3 0 1 0) (vector3 0 0 1)))
(define-param epsin 16.0)
(define-param epsout 1.0)
(define-param r1 0.13)
(define-param r2 0.13)
(define-param h (/ (sqrt 3) 2))

(define eps (make dielectric (epsilon epsin)))
(set! num-bands 40)
(set! resolution 32)

(define ax1 (vector3 1 1 1))
(define ax2 (vector3 -1 -1 1))
(define ax3 (vector3 1 -1 -1))
(define ax4 (vector3 -1 1 -1)) 

(define center1 (vector3 0.25 0.25 0.25))
(define center2 (vector3 -0.25 -0.25 0.25))
(define center3 (vector3 0.25 -0.25 -0.25))
(define center4 (vector3 -0.25 0.25 -0.25))

(define cylinder1 (make cylinder
                       (center center1) (radius r1) (height h) (axis ax1)
                       (material eps)))
(define cylinder2 (make cylinder
                       (center center2) (radius r2) (height h) (axis ax2)
                       (material eps)))
(define cylinder3 (make cylinder
                       (center center3) (radius r1) (height h) (axis ax3)
                       (material eps)))
(define cylinder4 (make cylinder
                       (center center4) (radius r2) (height h) (axis ax4)
                       (material eps)))

(set! geometry (list cylinder1 cylinder2 cylinder3 cylinder4) )

(set! k-points (list (vector3 0 0 0)     ; Gamma
                     (vector3 0.5 0 0)   ; X
		     (vector3 0.5 0.5 0) ; M
		     (vector3 0 0 0); Gamma	
                     (vector3 0.5 0.5 0.5) ; R
		     (vector3 0.5 0 0) ; X
		     (vector3 0.5 0.5 0); M
	             (vector3 0.5 0.5 0.5); R
))
(set! k-points (interpolate 100 k-points))
(run)


