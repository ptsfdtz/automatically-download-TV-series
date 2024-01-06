from selenium import webdriver

def get_full_html_with_js(url):
    try:
        options = webdriver.ChromeOptions()
        options.add_argument('--headless') 
        options.add_argument('--disable-gpu')
        driver = webdriver.Chrome(options=options)

        driver.get(url)

        full_html = driver.page_source

        return full_html

    except Exception as e:
        print(f"发生异常: {str(e)}")

    finally:
        driver.quit()

if __name__ == "__main__":
    target_url = "https://online.njtech.edu.cn/#/video/detail?id=5192"
    full_html = get_full_html_with_js(target_url)

    if full_html:
        print(full_html[:10000])
    else:
        print("未能获取完整 HTML 源代码。")
