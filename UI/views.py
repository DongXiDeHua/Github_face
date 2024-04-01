from typing import List
from UI import rootdata
from django.shortcuts import render, HttpResponse, redirect
from django.db import models
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from msedge.selenium_tools import Edge, EdgeOptions
from selenium.webdriver.edge.options import Options
from UI import models
from django.contrib import messages


# Create your views here.

def index1(request):
    return redirect("/index/")


def index(request):
    if request.method == "GET":
        return render(request, "index.html")
    user_name = request.session.get("user_name")
    name = request.POST.get("uname")
    password = request.POST.get("psw")
    from UI.models import UserInfo
    result = UserInfo.objects.filter(name=name, password=password).first()
    if result is not None:
        request.session["user_name"] = name
        request.session.set_expiry(0)
        return redirect("/index/user_index/")
    return render(request, "index.html", {"error_msg": "用户名或密码错误！请重新输入。", "user_name": user_name})


def register(request):
    if request.method == "GET":
        return render(request, "register.html")
    uname = request.POST.get("uname")
    password = request.POST.get("psw")
    from UI.models import UserInfo
    result = UserInfo.objects.filter(name=uname)
    if not result:
        UserInfo.objects.create(name=uname, password=password)
        # 删除东西 .update()更新
        # UserInfo.objects.filter(id=3).delete()
        # UserInfo.objects.all().delete()
        print(uname, password)
        return render(request, "index.html", {"error_msg": "您已经注册成功了！请登录"})
    return render(request, "register.html", {"error_msg": "注册失败！用户名已存在。"})


def user_cookie_delete(request):
    del request.session["user_name"]
    return redirect("/index/")


def root_cookie_delete(request):
    del request.session["root_name"]
    return redirect("/root/")


def root(request):
    if request.method == "GET":
        return render(request, "root.html", {"error_msg": "请登录管理员账号！"})
    rname = request.POST.get("rname")
    password = request.POST.get("psw")
    from UI.models import RootInfo
    result = RootInfo.objects.filter(name=rname, password=password).first()
    print(result)
    if result is not None:
        request.session["root_name"] = result.name
        return redirect("/root/index/")
    return render(request, "root.html", {"error_msg": "用户名或密码错误！"})


def root_index(request):
    root_name = request.session.get("root_name")
    if root_name is None:
        messages.success(request, "您还没有登录管理员账号！")
        return redirect("/root/", {"error_msg": "请登录管理员账号！"})
    print(root_name)
    return render(request, "root_index.html", {"root_name": str(root_name)})


def user_index(request):
    user_name = request.session.get("user_name")
    if user_name is None:
        messages.success(request, "您还没有登录！")
        return redirect("/index/", {"error_msg": "请先登录！"})
    return render(request, "user_index.html", {"user_name": user_name})


def change_password(request):
    user_name = request.session.get("user_name")
    if request.method == "GET":
        if user_name is None:
            messages.success(request, "您还没有登录！")
            return redirect("/index/", {"error_msg": "请先登录！"})
    name = request.POST.get("name")
    new_password = request.POST.get("new_password")
    new_password_repeat = request.POST.get("new_password_repeat")
    if name != user_name:
        return render(request, "change_password.html", {"error_msg": "您只能修改自己的密码！", "user_name": user_name})
    if new_password != new_password_repeat:
        return render(request, "change_password.html", {"error_msg": "两次密码输人不一致！", "user_name": user_name})
    try:
        from UI.models import UserInfo
        info = UserInfo.objects.get(name=name)
        info.password = new_password_repeat
        info.save(update_fields=['password'])
        return render(request, "user_index.html", {"error_msg": "更新密码成功！", "user_name": user_name})
    except:
        return render(request, "change_password.html", {"error_msg": "数据库操作失败！！", "user_name": user_name})


def user_manage(request):
    root_name = request.session["root_name"]
    if root_name is None:
        messages.success(request, "您还没有登录！")
        return redirect("/root/", {"error_msg": "请先登录！"})
    from UI.models import UserInfo
    user_list = UserInfo.objects.all()
    return render(request, "user_manage.html",
                  {"root_name": root_name, "user_list": user_list})


def reptile_manage(request):
    return HttpResponse("reptile_manage")


def face_manage(request):
    return HttpResponse("face_manage")


def sum_manage(request):
    return HttpResponse("sum_manage")


def user_delete(request):
    uid = request.GET.get('uid')
    from UI.models import UserInfo
    UserInfo.objects.filter(id=uid).delete()
    return redirect("/root/root_index/user_manage/")


def reptile(request):
    user_name = request.session.get("user_name")
    if request.method == 'GET':
        if user_name is None:
            messages.success(request, "您还没有登录！")
            return redirect("/index/", {"error_msg": "请先登录！"})
        return render(request, "reptile.html", {"user_name": user_name})
    name = request.POST.get("name")
    password = request.POST.get("psw")
    website = request.POST.get("website", None)
    from UI import models
    if website == "bilibili":
        if models.rootbili(name, password):
            return render(request, "reptile.html", {"error_msg": "爬取完成！"})
        return render(request, "reptile.html", {"error_msg": "用户或密码错误！"})


def reptile_view(request):
    user_name = request.session.get("user_name")
    if user_name is None:
        messages.success(request, "您还没有登录！")
        return redirect("/index/", {"error_msg": "请先登录！"})
    data_list = {}
    from UI.models import RootBilibili
    result = RootBilibili.objects.filter(user_name=user_name)
    for aim in result:
        if aim.aim_name in data_list:
            data_list[aim.aim_name] += 1
            print(aim.aim_name)
        else:
            data_list[aim.aim_name] = 1
            print(aim.aim_name)
    key_list = data_list.keys()
    print(key_list)
    if len(key_list) == 0:
        return render(request, "reptile_view.html", {"user_name": user_name, "error_msg": "未找到爬取数据！"})
    return render(request, "reptile_view.html", {"user_name": user_name, "key_list": key_list})


def reptile_view_post(request):
    user_name = request.session.get("user_name")

    if user_name is None:
        messages.success(request, "您还没有登录！")
        return redirect("/index/", {"error_msg": "请先登录！"})

    if request.method == "GET":
        return render(request, "reptile_view.html", {"error_msg": "请先选择查询名称！"})
    aim_name = request.POST.get("aim_name_post")

    from UI.models import RootBilibili

    result_label = RootBilibili.objects.filter(aim_name=aim_name, user_name=user_name)

    data_sum = {}
    # score_sum = {}

    for data in result_label:
        if data.label in data_sum:
            data_sum[data.label] += 1
        else:
            data_sum[data.label] = 1

    # for data in data_sum:
    #     result_score = LabelScore.objects.filter(label=data.key)
    #     score_sum[data.key] = int(result_score.score) * data.value
    #
    print(data_sum)
    return render(request, "reptile_view_post.html",
                  {"data_sum": data_sum, "result_label": result_label})  # , "score_sum": score_sum


def face(request):
    user_name = request.session.get("user_name")
    if user_name is None:
        messages.success(request, "您还没有登录！")
        return redirect("/index/", {"error_msg": "请先登录！"})
    return render(request, "face.html", {"user_name": user_name})


def face_view(request):
    user_name = request.session.get("user_name")
    if user_name is None:
        messages.success(request, "您还没有登录！")
        return redirect("/index/", {"error_msg": "请先登录！"})
    return render(request, "face_view.html", {"user_name": user_name})


def face_view_post(request):
    return render(request, "face_view_post.html")


def rootbilibili(request):
    user_name = request.session.get("user_name")
    if request.method == 'GET':
        if user_name is None:
            messages.success(request, "您还没有登录！")
            return redirect("/index/", {"error_msg": "请先登录！"})
        return render(request, "rootbilibili.html", {"user_name": user_name})

    def rootbili(name, password, aim_name, user_name):
        global driver
        try:
            from UI.models import RootBilibili
            driver = Edge()
            driver.maximize_window()

            # driver = webdriver.Chrome()

            aList = []  # 数据库准备

            driver.get('https://www.bilibili.com/')
            driver.implicitly_wait(10)
            driver.find_element_by_xpath(
                '//*[@id="i_cecream"]/div[2]/div[1]/div[1]/ul[2]/li[1]/li/div/div/span').click()
            driver.find_element_by_xpath('/html/body/div[4]/div/div[4]/div[2]/form/div[1]/input').click()
            driver.find_element_by_xpath('/html/body/div[4]/div/div[4]/div[2]/form/div[1]/input').send_keys(name)
            driver.find_element_by_xpath('/html/body/div[4]/div/div[4]/div[2]/form/div[3]/input').click()
            driver.find_element_by_xpath('/html/body/div[4]/div/div[4]/div[2]/form/div[3]/input').send_keys(password)
            driver.find_element_by_xpath('/html/body/div[4]/div/div[4]/div[2]/div[2]/div[2]').click()
            time.sleep(1)
            # driver.find_element_by_xpath('/html/body/div[3]/div/div[4]/div[2]/form/div[1]').click()
            # driver.find_element_by_xpath('/html/body/div[5]/div/div[4]/div[2]/form/div[1]').send_keys('13970069700')
            # driver.find_element_by_xpath('/html/body/div[5]/div/div[4]/div[2]/form/div[3]').click()
            # driver.find_element_by_xpath('/html/body/div[5]/div/div[4]/div[2]/form/div[3]').send_keys('qyh20020314!!!')
            # driver.find_element_by_xpath('/html/body/div[5]/div/div[4]/div[2]/div[2]/div[2]').click()
            yes = input('请继续登录，登录成功后回车确认：')
            if yes == "2":
                driver.close()
                return False
            driver.switch_to.window(driver.window_handles[0])
            new_url = driver.current_url
            print(new_url)
            driver.get(new_url)
            time.sleep(3)
            driver.find_element_by_xpath('//*[@id="i_cecream"]/div[2]/div[1]/div[1]/ul[2]/li[5]/a').click()
            driver.implicitly_wait(10)
            driver.switch_to.window(driver.window_handles[1])
            new_url = driver.current_url
            print(new_url)
            driver.get(new_url)
            time.sleep(2)
            new_selector = driver.page_source
            soup = BeautifulSoup(new_selector, 'html.parser')
            soup.prettify()
            # app > div.bili-dyn-home--member > main > section:nth-child(3) > div.bili-dyn-list > div.bili-dyn-list__items > div:nth-child(19)
            try:
                for i in range(10):
                    driver.execute_script('window.scrollTo(0,document.body.scrollHeight)')
                    time.sleep(0.5)
                for j in range(2, 80):
                    new_hrefs = soup.select(
                        # #history_list > li:nth-child(2) > div.r-info.clearfix > div.r-txt > a
                        # #history_list > li:nth-child(3) > div.r-info.clearfix > div.r-txt > a
                        # #history_list > li:nth-child(136) > div.r-info.clearfix > div.r-txt > a
                        '#history_list > li:nth-child({}) > div.r-info.clearfix > div.r-txt > a'.format(
                            j))
                    new_href = new_hrefs[0]['href']
                    aList.append('https:' + new_href)
                    print(aList)
            except:
                for url in aList:
                    new_url = str(url)
                    driver.get(new_url)
                    time.sleep(3)
                    new_selector = driver.page_source
                    soup = BeautifulSoup(new_selector, 'html.parser')
                    soup.prettify()
                    for i in range(10):
                        try:
                            labels = soup.select(
                                # #v_tag > div > div:nth-child(1)
                                # #v_tag > div > div:nth-child(2)
                                '#v_tag > div > div:nth-child({}) > div > a'.format(i))
                            label = labels[0].get_text().split()
                            RootBilibili.objects.create(label=str(label).replace("['", "").replace("']", ""),
                                                        user_name=user_name, aim_name=aim_name)
                            print(label, user_name, aim_name)
                        except:
                            print('')
            for url in aList:
                new_url = str(url)
                driver.get(new_url)
                time.sleep(3)
                new_selector = driver.page_source
                soup = BeautifulSoup(new_selector, 'html.parser')
                soup.prettify()
                for i in range(10):
                    try:
                        labels = soup.select(
                            # #v_tag > div > div:nth-child(1)
                            # #v_tag > div > div:nth-child(2)
                            '#v_tag > div > div:nth-child({}) > div > a'.format(i))
                        label = labels[0].get_text().split()
                        RootBilibili.objects.create(label=str(label).replace("['", "").replace("']", ""),
                                                    user_name=user_name, aim_name=aim_name)
                        print(label, user_name, aim_name)
                    except:
                        print('')
            driver.close()
            driver.quit()
            return True
        except:
            driver.close()
            driver.quit()
            return False

    name = request.POST.get("name")
    password = request.POST.get("psw")
    aim_name = request.POST.get("aim_name")
    request.session["aim_name"] = aim_name
    from UI.models import RootBilibili
    try:
        result = models.RootBilibili.objects.get(user_name=name, aim_name=aim_name)
        return render(request, "rootbilibili.html",
                      {"error_msg": "用户您好！您已经使用过这个目标名称！"})
    except RootBilibili.DoesNotExist:
        if rootbili(name, password, aim_name, user_name):
            rootdata.root_data(aim_name, user_name)
            return render(request, "rootbilibili_T.html", {"error_msg": "爬取完成！"})
        return render(request, "rootbilibili.html",
                      {"error_msg": "错误！请检查用户和密码！如反复如此，请联系管理员！"})


def rootbilibili_T(request):
    user_name = request.session.get("user_name")
    if request.method == 'GET':
        if user_name is None:
            messages.success(request, "您还没有登录！")
            return redirect("/index/", {"error_msg": "您还没有登录！请先登录！"})
        from UI.models import RootBilibili
        aim_name = request.session.get("aim_name")
        root_data_list = RootBilibili.objects.filter(aim_name=aim_name, user_name=user_name)
        if root_data_list is None:
            return render(request, "rootbilibili_T.html", {"user_name": user_name, "root_data_list": root_data_list,
                                                           "total_sum": "尚未爬取到如何数据！"})
        total_sum = {}
        for root_data in root_data_list:
            if root_data.label in total_sum:
                total_sum[root_data.label] = +1
                print(root_data.label)
            else:
                total_sum[root_data.label] = 1
                print(root_data.label)
        return render(request, "rootbilibili_T.html",
                      {"user_name": user_name, "root_data_list": root_data_list, "total_sum": total_sum,
                       "aim_name": aim_name})


def userbilibili(request):
    user_name = request.session.get("user_name")
    if request.method == 'GET':
        if user_name is None:
            messages.success(request, "您还没有登录！")
            return redirect("/index/", {"error_msg": "请先登录！"})
        return render(request, "userbilibili.html", {"user_name": user_name})

    def userbili(duser_name, daim_name, dname):
        global driver
        try:
            from UI.models import UserBilibili
            options = EdgeOptions()
            options.add_argument('--mute-audio')
            options.add_argument('--disable-infobars')
            options.add_argument("--start-muted")

            driver = Edge(options=options)
            driver.maximize_window()

            # driver = webdriver.Chrome()

            aList = []  # 数据库准备

            driver.get('https://www.bilibili.com/')
            driver.implicitly_wait(10)
            driver.find_element_by_xpath(
                '//*[@id="nav-searchform"]/div[1]').click()
            driver.find_element_by_xpath('//*[@id="nav-searchform"]/div[1]').send_keys(dname)
            driver.find_element_by_xpath('//*[@id="nav-searchform"]/div[2]').click()

            driver.implicitly_wait(10)
            time.sleep(1)
            driver.switch_to.window(driver.window_handles[0])
            new_url = driver.current_url
            print(new_url)
            driver.get(new_url)
            time.sleep(3)

            driver.find_element_by_xpath('//*[@id="i_cecream"]/div/div[2]/div[1]/div[2]/div/nav/ul/li[7]/span').click()

            driver.implicitly_wait(10)
            time.sleep(1)
            driver.switch_to.window(driver.window_handles[0])
            new_url = driver.current_url
            print(new_url)
            driver.get(new_url)
            time.sleep(2)

            driver.find_element_by_xpath(
                '//*[@id="i_cecream"]/div/div[2]/div[2]/div/div/div[2]/div[1]/div[1]/div/div/h2/a').click()

            driver.implicitly_wait(10)
            time.sleep(1)
            driver.switch_to.window(driver.window_handles[1])
            new_url = driver.current_url
            print(new_url)
            driver.get(new_url)
            time.sleep(2)
            new_selector = driver.page_source
            soup = BeautifulSoup(new_selector, 'html.parser')
            soup.prettify()
            try:
                birthdays = soup.select(
                    '#page-index > div.col-2 > div.section.user-info > div > div > div:nth-child(2) > span.info-value')
                birthday = birthdays[0].get_text().split()
                print(birthday)
            except:
                print('该用户未填写生日！')
            try:
                for i in range(1, 9):
                    new_hrefs = soup.select(
                        # #history_list > li:nth-child(2) > div.r-info.clearfix > div.r-txt > a
                        # #history_list > li:nth-child(3) > div.r-info.clearfix > div.r-txt > a
                        # #page-index > div.col-1 > div:nth-child(6) > div > div:nth-child(2) > a:nth-child(2)
                        '#page-index > div.col-1 > div:nth-child(6) > div > div:nth-child({}) > a:nth-child(2)'.format(
                            i))
                    new_href = new_hrefs[0]['href']
                    aList.append('https:' + new_href)
                    print(aList)
            except:
                for url in aList:
                    new_url = str(url)
                    driver.get(new_url)
                    time.sleep(3)
                    new_selector = driver.page_source
                    soup = BeautifulSoup(new_selector, 'html.parser')
                    soup.prettify()
                    for i in range(10):
                        try:
                            labels = soup.select(
                                # #v_tag > div > div:nth-child(1)
                                # #v_tag > div > div:nth-child(2)
                                '#v_tag > div > div:nth-child({}) > div > a'.format(i))
                            label = labels[0].get_text().split()
                            UserBilibili.objects.create(label=str(label).replace("['", "").replace("']", ""),
                                                        user_name=user_name, aim_name=aim_name)
                            print(label, user_name, aim_name)
                        except:
                            print('')
            for url in aList:
                new_url = str(url)
                driver.get(new_url)
                time.sleep(3)
                new_selector = driver.page_source
                soup = BeautifulSoup(new_selector, 'html.parser')
                soup.prettify()
                for i in range(10):
                    try:
                        labels = soup.select(
                            # #v_tag > div > div:nth-child(1)
                            # #v_tag > div > div:nth-child(2)
                            '#v_tag > div > div:nth-child({}) > div > a'.format(i))
                        label = labels[0].get_text().split()
                        UserBilibili.objects.create(label=str(label).replace("['", "").replace("']", ""),
                                                    user_name=user_name, aim_name=aim_name)
                        print(label, user_name, aim_name)
                    except:
                        print('')
            driver.quit()
            return True
        except:
            driver.quit()
            return False

    name = request.POST.get("name")
    aim_name = request.POST.get("aim_name")
    result = models.UserBilibili.objects.filter(user_name=name, aim_name=aim_name)
    if not result:
        if userbili(user_name, aim_name, name):
            return render(request, "userbilibili_T.html", {"error_msg": "爬取完成！"})
        return render(request, "userbilibili.html",
                      {"error_msg": "遇到错误！请检查用户名后重新尝试！如果反复如此，请联系管理员！"})
    return render(request, "rootbilibili.html",
                  {"error_msg": "用户您好！您已经使用过这个目标名称！"})


def QQspace(request):
    user_name = request.session.get("user_name")
    if request.method == 'GET':
        if user_name is None:
            messages.success(request, "您还没有登录！")
            return redirect("/index/", {"error_msg": "请先登录！"})
        return render(request, "QQspace.html", {"user_name": user_name})
    aim_name = request.POST.get("aim_name")
    name = request.POST.get("name")
    psw = request.POST.get("psw")
    aim_qq = request.POST.get("aim_qq")

    def QQspace_reptile(aim_name, name, psw, aim_qq, user_name):
        global driver
        try:
            from UI.models import Aim
            options = EdgeOptions()
            options.add_argument('--mute-audio')
            options.add_argument('--disable-infobars')
            options.add_argument("--start-muted")

            driver = Edge(options=options)
            driver.maximize_window()

            # driver = webdriver.Chrome()

            aList = []  # 数据库准备

            driver.get('https://www.qzone.qq.com/')
            driver.implicitly_wait(10)
            driver.find_element_by_xpath('//*[@id="switcher_plogin"]').click()
            time.sleep(2)
            driver.find_element_by_xpath(
                '//*[@id="nav-searchform"]/div[1]').click()
            driver.find_element_by_xpath(
                '//*[@id="nav-searchform"]/div[1]').send_keys(name)
            driver.find_element_by_xpath('//*[@id="p"]').click()
            driver.find_element_by_xpath('//*[@id="p"]').send_keys(psw)
            driver.find_element_by_xpath('//*[@id="login_button"]').click()

        except:
            return False

        try:
            driver.implicitly_wait(10)
            time.sleep(1)
            driver.switch_to.window(driver.window_handles[0])
            new_url = driver.current_url
            print(new_url)
            driver.get(new_url)
            time.sleep(3)

            driver.get("https://user.qzone.qq.com/{}".format(aim_qq))
            driver.implicitly_wait(10)
            driver.find_element_by_xpath('//*[@id="menuContainer"]/div/ul/li[6]/a').click()
            driver.implicitly_wait(5)
            driver.find_element_by_xpath('//*[@id="info_link"]').click()
        except:
            return False

        new_selector = driver.page_source
        soup = BeautifulSoup(new_selector, 'html.parser')
        soup.prettify()
        try:
            sexs = soup.select('#sex')
            sex = sexs[0].get_text().split()
        except Exception:
            pass
        try:
            age = soup.select('//*[@id="age"]')[0].get_text().split()
        except Exception:
            pass
        try:
            birthday = soup.select('//*[@id="birthday"]')[0].get_text().split()
        except Exception:
            pass
        try:
            qq_name = soup.select('#nickname_n')[0].get_text().split()
        except Exception:
            pass
        try:
            city = not soup.select('#live_address > span:nth-child(1)')[0].get_text().split()
        except Exception:
            pass
        try:
            user_name = name
            blood_type = soup.select('#blood')[0].get_text().split()
        except Exception:
            pass
        try:
            qq = aim_qq
            star_signs = soup.select('#astro')
            star_sign = star_signs[0].get_text().split()
        except Exception:
            pass
        try:
            Aim.objects.create(name=qq_name, user_name=user_name, birthday=birthday, city=city, phone=None,
                               blood_type=blood_type, gender=sex, age=age, star_sign=star_sign, QQ=aim_qq)
        except:
            return False
        driver.quit()
        driver.close()
        return True

    if QQspace_reptile(aim_name, name, psw, aim_qq, user_name):
        return render(request, "QQspace_T.html", {"user_name": user_name, "error_msg": "爬取成功！"})
    return render(request, "QQspace.html", {"user_name": user_name, "error_msg": "遇到错误！请重新尝试。"})


def rootxiaohongshu(request):
    user_name = request.session.get("user_name")
    if request.method == 'GET':
        if user_name is None:
            messages.success(request, "您还没有登录！")
            return redirect("/index/", {"error_msg": "请先登录！"})
        return render(request, "userbilibili.html", {"user_name": user_name})


def userxiaohongshu(request):
    user_name = request.session.get("user_name")
    if request.method == 'GET':
        if user_name is None:
            messages.success(request, "您还没有登录！")
            return redirect("/index/", {"error_msg": "请先登录！"})
        return render(request, "userbilibili.html", {"user_name": user_name})
    name = request.POST.get("name")
    password = request.POST.get("psw")
    from UI import models
