import random


async def human_like_actions(page):
    """人类行为模拟器"""
    # 随机等待
    await page.wait_for_timeout(random.randint(800, 2500))

    # 鼠标移动模式
    for _ in range(random.randint(2, 5)):
        await page.mouse.move(
            random.randint(0, 1600),
            random.randint(0, 900),
            steps=random.randint(5, 20)
        )
        await page.wait_for_timeout(random.randint(100, 500))

    # 页面滚动
    await page.evaluate(f"""
        window.scrollTo({{
            top: {random.randint(300, 2000)},
            behavior: 'smooth'
        }})
    """)
