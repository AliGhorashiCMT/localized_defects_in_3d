epsilon = h5read("lattice-epsilon.h5", "/data");
nx = 1; ny = 1; nz = 1;
eps_big = repmat(epsilon, [nx, ny, nz]);

eps_big(1:10, 1:10, 1:10) =0;
eps_big(1:10, (32-10):32, (32-10):32) =0;
eps_big((32-10):32, 1:10, (32-10):32) =0;
eps_big((32-10):32, (32-10):32, 1:10) =0; % This and the three lines above it are to get rid of annoying intersections of cylinders 
% from other unit cells edging into the center unit cell. 

max_epsilon = max(epsilon, [], 'all');
min_epsilon = min(epsilon, [], 'all');
level = (max_epsilon+min_epsilon)/2;
figure;
p = patch(isosurface(eps_big, level));
p.FaceColor = 'flat';
p.EdgeColor = 'none';
p.FaceAlpha = 1;

camlight; lighting gouraud;
material dull

axis equal
view(35,25)

hold on 

delta = 0;
plot3([1+delta, 32+delta, 32+delta, 1+delta, 1+delta], [1+delta, 1+delta, 32+delta, 32+delta, 1+delta], [1+delta, 1+delta, 1+delta, 1+delta, 1+delta], "-r", 'Linewidth', 2)

plot3([1+delta, 32+delta, 32+delta, 1+delta, 1+delta], [1+delta, 1+delta, 32+delta, 32+delta, 1+delta], [32+delta, 32+delta, 32+delta, 32+delta, 32+delta], "-r", 'Linewidth', 2)

plot3([1+delta, 1+delta], [1+delta, 1+delta], [1+delta, 32+delta], "-r", 'Linewidth', 2);
plot3([32+delta, 32+delta], [1+delta, 1+delta], [1+delta, 32+delta], "-r", 'Linewidth', 2);
plot3([1+delta, 1+delta], [32+delta, 32+delta], [1+delta, 32+delta], "-r", 'Linewidth', 2);
plot3([32+delta, 32+delta], [32+delta, 32+delta], [1+delta, 32+delta], "-r", 'Linewidth', 2);
lim_1 = 16-5; 
lim_2 = 16+5;
xticks([]) 
yticks([]) 
zticks([]) 

x = [1 1 32 32]; 
y = [1 32 32 1]; 
z_1 = [1 1 1 1];
z_2 = [32 32 32 32]; 

fill3(x, y, z_1, 'r', 'FaceAlpha', 0.2) 
fill3(x, y, z_2, 'r', 'FaceAlpha', 0.2) 
fill3(x, z_1, y, 'r', 'FaceAlpha', 0.2) 
fill3(x, z_2, y, 'r', 'FaceAlpha', 0.2) 
fill3(z_1, x, y, 'r', 'FaceAlpha', 0.2) 
fill3(z_2, x, y, 'r', 'FaceAlpha', 0.2) 
xlim([-32, 64]); ylim([-32, 64]); zlim([-32, 64]) % This is to make sure there's more of the white background
box off
exportgraphics(gcf, 'unit_cell.pdf', 'Resolution', 1000)