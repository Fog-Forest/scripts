#!/usr/bin/python3
# coding=utf8
# @Author: Kinoko <admin@amogu.cn>
# @Date  : 2022/01/26
# @Desc  : MacCMS 扩展分类自动处理去重

import pymysql

# 数据库连接信息
DBHost = "127.0.0.1"
DBName = "movie"
DBUser = "movie"
DBPasswd = "xxxxxxx"
# 关键字替换信息
# 地域
area_replace_words1 = {" / ": ",", "/": ",", "，": ",", "日韩地区": "日本,韩国", "日韩": "日本,韩国", "欧美其他": "美国,其他",
                       "港台": "中国香港,中国台湾"}
area_replace_words2 = {"2004": "", "2006": "", "2009": "", "开通视频会员": "其他", "内详": "其他", "换一换": "其他", "在线观看": "其他",
                       "其它": "其他", "未知": "其他", "澳大利亚 Australia": "澳大利亚", "印度 Indian": "印度", "荷兰 The Netherlands": "荷兰",
                       "马来西亚 Malaysia": "马来西亚", "印度indian": "印度", "俄国 Russia": "俄国", "英国 UK": "英国", "欧美": "美国",
                       "乌拉圭 Uruguay": "乌拉圭", "印尼 Indonesia": "印度尼西亚", "巴西Brazil": "巴西", "西德  West Germany": "德国",
                       "保加利亚 Bulgaria": "保加利亚", "挪威 Norway": "挪威", "加拿大 Canada": "加拿大", "tvb": "中国香港", "[db:地区]": "",
                       "美國USA": "美国", "菲律宾 Philippines": "菲律宾", "南非 South Africa": "南非", "印度 India": "印度",
                       "阿根廷 Argentina": "阿根廷", "台灣 Taiwan": "中国台湾", "馬來西亞 Malaysia": "马来西亚", "瑞士  Switzerland": "瑞士",
                       "奥地利 Austria": "奥地利", "U.S.A": "美国", "阿根廷 Arge": "阿根廷", "俄罗斯Russia": "俄罗斯",
                       "南非SouthAfrica": "南非", "菲律賓 Philippines": "菲律賓", "中国澳门": "澳门", "委内瑞拉 Venezuela": "委内瑞拉",
                       "加拿大Canada": "加拿大", "希腊 Greece": "希腊", "澳大利亚Australia": "澳大利亚", "俄罗斯 Russia": "俄罗斯",
                       "新西兰 New Zealand": "新西兰", "其他地区": "其他", "其它地区": "其他", "大陆": "中国大陆", "暂无": "其他", "美国 USA": "美国",
                       "国产剧": "中国大陆", "日本 Japan": "日本", "瑞典 Sweden": "瑞典", "印度 india": "印度", "加拿大  Canada": "加拿大",
                       "新加坡 Singapore": "新加坡", "爱尔兰 Ireland": "爱尔兰", "香港地区": "中国香港", "香港": "中国香港",
                       "荷兰Netherlands": "荷兰", "内地": "中国大陆", "中国": "中国大陆", "国产": "中国大陆", "澳门": "中国澳门", "Germany": "德国",
                       "芬兰 Finland": "芬兰", "Slovakia": "斯洛伐克", "The Grand Farewell": "德国", "India": "印度", "South": "美国",
                       "台湾": "中国台湾", "加拿大 Ca": "加拿大", "荷兰 Netherlands": "荷兰", "欧美地区": "美国", "国漫": "中国大陆",
                       "南斯拉夫 Yugoslavia": "南斯拉夫", "不详": "其他", "Italy": "意大利", "华语": "中国大陆", "Slovenia": "斯洛文尼亚",
                       "国内": "中国大陆", "马拉西亚": "马来西亚", "Costa": "哥斯达黎加", "UK": "英国", "保加利亚 Bu": "保加利亚",
                       "Palestine": "巴勒斯坦", "伊朗 Iran": "伊朗", "西德": "德国", "美国地区": "美国", "埃塞俄比亚Ethiopia": "埃塞俄比亚",
                       "中国大陆大陆剧": "中国大陆", "泰國": "泰国", "保加利": "保加利亚", "意": "意大利", "法": "法国", "美": "美国", "Denmark": "丹麦",
                       "中": "中国大陆", "Mexico": "墨西哥", "白俄罗斯": "俄罗斯", " ": ""}
area_retain_words = ["中国大陆", "中国香港", "中国台湾", "中国澳门", "美国", "法国", "意大利", "亚美尼亚", "奥法利亚", "保加利亚"]
# 扩展分类
class_replace_words1 = {"片": ",", "纪录-探索": "记录,探索", "纪录-科技": "纪录,科技", "纪录-自然": "纪录,自然", "纪录-人物": "纪录,人物",
                        "纪录-历史": "纪录,历史", "纪录-文化": "纪录,文化", "纪录-解密": "纪录,解密", "纪录-军事": "纪录,军事", "纪录-其它": "纪录,其他",
                        "人文历史": "人文,历史", "游戏互动": "游戏,互动", "怀旧经典": "怀旧,经典", "预告&剧八卦": "预告,八卦", "预告&amp;剧八卦": "预告,八卦",
                        "游戏竞技": "游戏,竞技", "情感交友": "情感,交友", "悬疑推理": "悬疑,推理", "动漫音乐": "动漫,音乐", "真人特摄": "真人,特摄",
                        "儿童奇幻": "儿童,奇幻", "儿童益智": "儿童,益智", "儿童教育": "儿童,教育", "儿童搞笑": "儿童,搞笑", "儿童音乐": "儿童,音乐",
                        "儿童历险": "儿童,历险", "儿童竞技": "儿童,竞技", "少儿资讯": "少儿,资讯", "早教益智": "早教,益智", "明星访谈": "明星,访谈",
                        "相声小品": "相声,小品", "生活服务": "生活,服务", "潮流文化": "潮流,文化", "学英语": "学习,英语", "女神办公室": "职场,女神",
                        "青春偶像": "青春,偶像", "舞台艺术": "舞台,艺术", "单人脱口秀": "单人,脱口秀", "美式脱口秀": "美式,脱口秀", "意见反馈": "意见,反馈",
                        "棚内真人秀": "棚内,真人秀", "少儿经典": "少儿,经典", "相声评书": "相声,评书"}
class_replace_words2 = {"电影-情": "剧情", "电影-喜": "喜剧", "电影-网络电影": "网络", "电影-动画电影": "动画", "电视-情": "剧情", "电视-喜": "喜剧",
                        "动漫-爆笑": "搞笑", "动漫-动画电影": "剧场版", "电影-": "", "电视-": "", "综艺-": "", "动漫-": "", "播报-": "",
                        "Animation": "动画", "Drama": "剧情", "Fantasy": "奇幻", "Family": "家庭", "Romance": "爱情",
                        "Adventure": "冒险", "Kids": "少儿", "Documentary": "记录", "History": "历史", "War": "战争",
                        "Action": "动作", "Mystery": "悬疑", "Sci-Fi": "科幻", "Reality-TV": "真人秀", "Game-Show": "游戏",
                        "News": "资讯", "LOLI": "萝莉", "电视（B站）": "哔哩哔哩", "电影（B站）": "哔哩哔哩", "番（B站）": "番剧", "国创（B站）": "国创",
                        "0-3岁": "早教", "4-6岁": "少儿", "7-10岁": "儿童", "2006": "", "紀錄": "记录", "劇情": "剧情", "土豆映像": "土豆",
                        "出品": "", "美国剧": "美国", "台湾剧": "", "香港剧": "", "青春剧": "青春", "韩剧": "韩国", "泰剧": "泰国", "内地剧": "",
                        "海外剧": "", "日本剧": "日本", "日韩剧": "", "韩国剧": "韩国", "泰国剧": "泰国", "国产剧": "", "欧美剧": "", "港台剧": "",
                        "网络剧": "网络", "舞台剧": "舞台", "国产综艺": "", "内地综艺": "", "大陆综艺": "", "香港综艺": "",
                        "台湾综艺": "", "港台综艺": "", "日韩综艺": "", "欧美综艺": "", "少儿综艺": "少儿", "欧美动漫": "", "港台动漫": "",
                        "海外动漫": "", "日韩动漫": "番剧", "日本动漫": "番剧", "国产动漫": "国创", "泡面番": "泡面", "漫画改编": "漫画改", "动态漫画": "其他",
                        "中国大陆": "", "中国香港": "", "中国台湾": "", "大陆": "", "香港地区": "", "中国澳门": "", "西班牙SPain": "西班牙",
                        "网剧": "网络", "网综": "网络", "动漫电影": "动画", "华语": "", "普通话": "",
                        "动画电影": "动画", "黑色电影": "黑暗", "网络电影": "网络", "百度云电影重入": "", "美少女": "少女", "合家欢": "家庭",
                        "音乐节目": "音乐", "娱乐节目": "娱乐", "女孩": "少女", "好习惯": "习惯", "超级网络": "网络", "社会题材": "社会", "杜比音效": "音乐",
                        "返回首页": "", "惊栗": "惊悚", "竖版视频": "短剧", "加拿大": "", "内地": "", "竖短": "短剧", "短": "短片", "网": "网络",
                        "综艺": "", "电视剧": "", "暂无": "其他", "未知": "其他", "其它": "其他", "喜": "喜剧", "日韩": "", "港台": "",
                        "情色": "", "韩": "韩国", "日": "日本", "情": "爱情"}
class_retain_words = ["喜剧", "网络", "短剧", "短片", "韩国", "日本", "日常", "爱情", "情景", "剧情", "言情", "情感", "亲情"]


# 获取视频信息数据
def get_vod_data():
    db = pymysql.connect(host=DBHost, user=DBUser, password=DBPasswd, database=DBName)
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
    # SQL 查询语句
    sql = "SELECT vod_id,vod_class,vod_area FROM mac_vod ORDER BY vod_id DESC"
    try:
        cursor.execute(sql)
        # 获取所有记录列表
        results = cursor.fetchall()
        return results
    except:
        print("Error: unable to fetch data")
    # 关闭数据库连接
    db.close()


# 更新扩展分类数据
def update_vod_data(vod_id, vod_area, vod_class):
    # 如果地域信息为空则作为“其他”处理
    if vod_area == "":
        vod_area = "其他"
    else:
        pass
    # 如果扩展分类信息为空则作为“其他”处理
    if vod_class == "":
        vod_class = "其他"
    else:
        pass

    db = pymysql.connect(host=DBHost, user=DBUser, password=DBPasswd, database=DBName)
    cursor = db.cursor()
    # SQL 更新语句
    sql = 'UPDATE mac_vod SET vod_class="' + vod_class + '",vod_area="' + vod_area + '" WHERE vod_id=' + str(vod_id)
    print(sql)
    try:
        cursor.execute(sql)
        # 提交到数据库执行
        db.commit()
    except:
        # 发生错误时回滚
        db.rollback()
    # 关闭数据库连接
    db.close()


# 关键字处理（扩展分类和地域信息）
def data_process(data, task_type):
    temp = []

    # 判断任务类型 1：替换地域名称，2：替换扩展分类
    if task_type == 1:
        replace_words1 = area_replace_words1
        replace_words2 = area_replace_words2
        retain_words = area_retain_words
    elif task_type == 2:
        replace_words1 = class_replace_words1
        replace_words2 = class_replace_words2
        retain_words = class_retain_words
    else:
        replace_words1 = None
        replace_words2 = None
        retain_words = None

    times1 = len(replace_words1)  # 第一次遍历替换次数
    times2 = len(replace_words2)  # 第二次遍历替换次数

    # 遍历数据并处理
    for i in range(times1):  # 第一次替换
        data = data.replace(list(replace_words1.keys())[i], list(replace_words1.values())[i])
    for words in data.split(','):  # 第二次替换
        # 扩展分类关键字替换
        for j in range(times2):
            if words in retain_words:
                pass
            else:
                words = words.replace(list(replace_words2.keys())[j], list(replace_words2.values())[j])
        # 替换完成后塞入临时列表
        if words == "":
            pass
        else:
            temp.append(words)

    # 去重处理(重新整理扩展分类顺序)
    words_list = list(set(temp))
    words_str = ",".join(words_list)

    return words_str


# MAIN
def main():
    results = get_vod_data()
    # 遍历视频数据信息
    for data in results:
        vod_id = data[0]
        vod_area = data_process(data[2], 1)  # 地域
        vod_class = data_process(data[1], 2)  # 扩展分类
        update_vod_data(vod_id, vod_area, vod_class)  # 更新数据


if __name__ == "__main__":
    main()
