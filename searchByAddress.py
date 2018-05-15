# -*- coding: UTF-8 -*-

import pymysql

class search_by_address():


    def getValue(self, list):
        self.Elements = list
        # print("GOT VALUES")

    def run(self, list):
        self.getValue(list)
        conn = pymysql.connect(host='101.132.154.2',port=3306,user='housing',passwd='housing',db='housing',charset='utf8')
        # print("Connected To Database!")

        cursor = conn.cursor()
        sql = "select id,address,square,avg,floor,total,height,direction,built_year,guapai_month,abs(square-%s) as result from guapai_201708 where address like %s having result<10.0 union " \
              "select id,address,square,avg,floor,total,height,direction,built_year,guapai_month,abs(square-%s) as result from guapai_201709 where address like %s having result<10.0 union " \
              "select id,address,square,avg,floor,total,height,direction,built_year,guapai_month,abs(square-%s) as result from guapai_201710 where address like %s having result<10.0 " \
              "order by result asc ;";

        address = self.Elements[0]
        square = self.Elements[3]
        floor = self.Elements[1]
        direction = self.Elements[2]

        sum = 0
        cursor.execute(sql,(square, address+'%',square, address+'%',square, address+'%'))
        # fangYuan = cursor.fetchall()
        self.fangYuan = cursor.fetchmany(5)

        if cursor.rownumber == 0:
            print("Result NOT Found!")
            conn.close()
            cursor.close()
            return "No Result!"
        count = 0
        for each in self.fangYuan:
            print(each)

            #
            # modify each !!!
            # take average within modified price
            # return average price
            #
            sum += each[3]
            count += 1
        avg = float( sum / count )

        conn.close()
        cursor.close()
        print("Average Price:", avg)
        return avg


if __name__ == '__main__':
    search = search_by_address()
    search.run(['西藏南路1739弄', '10', '南', '103', '34', '2010'])
