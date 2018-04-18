from base import CutLoop, Routine

start = 0
end = 5

cl = CutLoop()
ins = range(start, end)
cl.run_on_list(ins)
