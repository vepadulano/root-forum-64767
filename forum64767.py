import ROOT
import numpy
import psutil

fnames = [f"data/{i}.root" for i in range(1, 6)]
tname = "trawvoltage"
nentries = 780 # Total number of entries across all files
entries_to_read = 50
# There is one cluster per file (visible via 'rootls -t file.root')
# These are the cluster boundaries taking into account the whole list of files
# i.e., these are global entry numbers
cluster_boundaries = [[0, 197], [197, 483], [483, 578], [578, 677], [677, 781]]
proc = psutil.Process()

def main():
    with proc.oneshot():
        last_mem_info = proc.memory_info()

    ch = ROOT.TChain(tname)
    for fname in fnames:
        ch.Add(fname)

    df = ROOT.RDataFrame(ch)
    with proc.oneshot():
        cur_mem_info = proc.memory_info()
        initial_mem_info = cur_mem_info
        delta_rss = cur_mem_info.rss - last_mem_info.rss
        last_mem_info = cur_mem_info
        print(f"Delta RSS before for loop: {delta_rss/1e6:.2f}")

# Uncomment the next few lines to run the for loop like in the forum post
# This is less efficient in terms of I/O because the ranges do not respect
# cluster boundaries. Thus, every cluster will be re-read multiple times and
# this may lead to a memory increase
#    for ij in range(numpy.ceil(nentries/entries_to_read).astype(int)):
#        begin = ij * entries_to_read
#        end = (ij + 1) * entries_to_read
#        end = end if end <= nentries else nentries
    for [begin, end] in cluster_boundaries:
        df.Range(begin, end).AsNumpy(["trace_ch"])
        print(f"{begin=},{end=}")
        with proc.oneshot():
            cur_mem_info = proc.memory_info()
            delta_rss = cur_mem_info.rss - last_mem_info.rss
            last_mem_info = cur_mem_info
            print(cur_mem_info)
            print(f"Delta RSS: {delta_rss/1e6:.2f}")

    with proc.oneshot():
        cur_mem_info = proc.memory_info()
        delta_rss = cur_mem_info.rss - initial_mem_info.rss
        print(f"Delta RSS w.r.t. before the for loop: {delta_rss/1e6:.2f}")

if __name__ == "__main__":
    raise SystemExit(main())
