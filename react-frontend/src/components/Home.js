import React from "react";

function Home() {
    return (
        <div>
            <h1>首頁</h1>
            <div className="home-container">
                <div className="home-left">
                    <h2>系統概況</h2>
                    <p>目前報名人數：30人</p>
                    <p>已提交作品數：10件</p>
                    <p>評分完成度：2/5 評審完成</p>
                    <h2>重要日期</h2>
                    <p>報名截止：2024/12/31</p>
                    <p>決賽日期：2025/01/15</p>
                </div>
                <div className="home-right">
                    <h2>最新公告</h2>
                    <ul className="announcement-list">
                        <li><a href="#">[2024/12/10] 比賽報名截止延長至12/31</a></li>
                        <li><a href="#">[2024/12/05] 新增作品上傳格式說明</a></li>
                        <li><a href="#">[2024/12/01] 評審名單公布</a></li>
                    </ul>
                </div>
            </div>
        </div>
    );
}

export default Home;
