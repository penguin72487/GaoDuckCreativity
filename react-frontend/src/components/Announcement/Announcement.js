import React, { useEffect, useState } from "react";
import axios from "axios";


const Announcement = () => {
    const [announcements, setAnnouncements] = useState([]);

    useEffect(() => {
        // 從後端獲取公告資料
        axios.get("http://127.0.0.1:5000/api/announcements")
            .then(response => {
                setAnnouncements(response.data); // 假設後端返回的資料是直接的列表
            })
            .catch(error => console.error("Error fetching announcements:", error));
    }, []);

    return (
        <div className="page">
            <h1>最新公告</h1>
            <ul className="announcement-list">
                {announcements.length > 0 ? (
                    announcements.map((announcement, index) => (
                        <li key={index} style={{ marginBottom: "1rem" }}>
                            <h3>{announcement.title}</h3>
                        </li>
                    ))
                ) : (
                    <li>目前沒有公告。</li>
                )}
            </ul>
        </div>
    );
};

export default Announcement;
