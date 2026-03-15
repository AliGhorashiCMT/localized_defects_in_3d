epsilon = h5read("supercell-5-1-20-16epsilon.h5", "/data"); % Corresponds to a radius of r=0.77;
nx = 1; ny = 1; nz = 1;
eps_big = repmat(epsilon, [nx, ny, nz]);
eps_big1 = eps_big;
eps_big1(40:80, 40:80, 40:80) = 0; % Cut out a corner of the supercell so that we can better see the spherical defect at the origin

max_epsilon = max(epsilon, [], 'all');
min_epsilon = min(epsilon, [], 'all');
level = (max_epsilon+min_epsilon)/2;
figure;
p = patch(isosurface(eps_big1, level));
p.FaceColor = 'flat';
p.EdgeColor = 'none';
p.FaceAlpha = 1;

defect_minus = 40-15;
defect_plus = 40+15;

eps_near_defect = zeros(80, 80, 80);

eps_near_defect(defect_minus:defect_plus, defect_minus:defect_plus, defect_minus:defect_plus) = eps_big(defect_minus:defect_plus, defect_minus:defect_plus, defect_minus:defect_plus);

[x,y,z] = ndgrid(1:80,1:80,1:80);

eps_near_defect((x-40.5).^2 + (y-40.5).^2 + (z-40.5).^2 > 12.5^2) = 0;
level2 = level;
p2 = patch(isosurface(eps_near_defect, level2));
p2.FaceColor = 'flat';
p2.EdgeColor = 'none';
p2.FaceAlpha = 1;

camlight; lighting gouraud;
material dull

axis equal
view(35,25)
xticks([]); yticks([]); zticks([]);

hold on 
xlim([-80, 120]); ylim([-80, 120]); zlim([-80, 120]) % This is to make sure there's more of the white background
box off
%exportgraphics(gcf, 'super_cell.pdf', 'Resolution', 1000)