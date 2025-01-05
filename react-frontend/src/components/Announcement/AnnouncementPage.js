import React, { useEffect, useState } from "react";
import axios from "axios";

const AnnouncementPage = () => {
    const [announcements, setAnnouncements] = useState([]);

    useEffect(() => {
        // 獲取所有公告資料
        axios.get("http://127.0.0.1:5000/api/announcements")
            .then(response => setAnnouncements(response.data.announcements))
            .catch(error => console.error("Error fetching announcements:", error));
    }, []);

    return (
        <div className="page">
            <h1>公告頁面</h1>
            <ul className="announcement-list">
                {announcements.length > 0 ? (
                    announcements.map((announcement, index) => (
                        <li key={index}>
                            <h3>{announcement.title}</h3>
                            <p>{announcement.information}</p>
                        </li>
                    ))
                ) : (
                    <li>目前沒有公告。</li>
                )}
            </ul>
        </div>
    );
};

export default AnnouncementPage;