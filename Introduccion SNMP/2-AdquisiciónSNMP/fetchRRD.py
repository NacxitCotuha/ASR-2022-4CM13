import rrdtool


if __name__ == "__main__":
    data = rrdtool.fetch("traficoRED.rrd", "AVERAGE", "-s","-15m", "-e", "-10m")
    start, end, step = data[0]
    print(f"start: {start}")
    print(f"end: {end}")
    print(f"step: {step}")
    
    ds = data[1]
    rows = data[2]
    print("DS")
    for dato in ds:
        print(ds)
    print("ROWS")
    for row in rows:
        print(row)