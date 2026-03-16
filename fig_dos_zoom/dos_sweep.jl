task_id, num_tasks = parse.(Int, ARGS)
println("task_id is $task_id")
println("num_tasks $num_tasks")
N = 100
kpoints = Vector{Float64}[]
for ky_idx in 1:N
	ky = -0.5 + ky_idx/N
	for kz_idx in 1:N	
		kz = -0.5 + kz_idx/N
		push!(kpoints, [0.5 + ky/10, 0.5 + kz/10])
        end
end

for id in task_id:num_tasks:length(kpoints)
	ky, kz = kpoints[id]
	run(`./runlattice.sh $ky $kz $id`)
end
