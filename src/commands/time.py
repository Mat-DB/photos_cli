from functions import adjust_time


def time(args):
    print("time function -> to implement")
    if args.fullTime:
        new_date = adjust_time.asking_new_date
    else:
        print("time will be adjust with time", args.time_adj)
