import csv
def 读取所有数据():
    try:
        with open("批记录.csv",mode="r",encoding="utf-8") as 文件:
            阅读器=csv.reader(文件)
            表头_=next(阅读器)
            return list(阅读器)
    except FileNotFoundError:
        return []
def 追加记录(批号,收率,结果):
    with open("批记录.csv",mode="a",newline="",encoding="utf-8") as 文件:
        写入器=csv.writer(文件)
        if 文件.tell()==0:
            写入器.writerow(["批号","收率","结果"])
        写入器.writerow([批号,收率,结果])
def 查找批号(批号):
    try:
        with open("批记录.csv",mode="r",encoding="utf-8") as 文件:
            reader=csv.reader(文件)
            表头_=next(reader)
            for i in reader:
                if i[0]==批号:
                    批信息=[批号,i[1],i[2]]
                    return 批信息
            return []
    except FileNotFoundError:
        return []
 
        
