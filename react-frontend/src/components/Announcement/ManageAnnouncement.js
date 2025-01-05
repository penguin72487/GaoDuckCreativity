import React, { useState, useEffect } from "react";
import axios from "axios";

const ManageAnnouncement = () => {
    const [announcements, setAnnouncements] = useState([]); // 初始化為空數組
    const [newAnnouncement, setNewAnnouncement] = useState("");
    const [editAnnouncement, setEditAnnouncement] = useState({ id: null, content: "" });

    useEffect(() => {
        // 獲取現有公告
        axios.get("http://127.0.0.1:5000/api/announcements")
            .then(response => setAnnouncements(response.data.announcements || [])) // 確保是數組
            .catch(error => console.error("Error fetching announcements:", error));
    }, []);

    const handleAddAnnouncement = () => {
        if (!newAnnouncement.trim()) {
            alert("公告內容不能為空！");
            return;
        }

        axios.post("http://127.0.0.1:5000/api/announcements", { content: newAnnouncement })
            .then(response => {
                setAnnouncements([...announcements, response.data.announcement]);
                setNewAnnouncement("");
            })
            .catch(error => console.error("Error adding announcement:", error));
    };

    const handleDeleteAnnouncement = (id) => {
        axios.delete(`http://127.0.0.1:5000/api/announcements/${id}`)
            .then(() => {
                setAnnouncements(announcements.filter(announcement => announcement.id !== id));
            })
            .catch(error => console.error("Error deleting announcement:", error));
    };

    const handleEditAnnouncement = (id, content) => {
        setEditAnnouncement({ id, content });
    };

    const handleUpdateAnnouncement = () => {
        if (!editAnnouncement.content.trim()) {
            alert("公告內容不能為空！");
            return;
        }

        axios.put(`http://127.0.0.1:5000/api/announcements/${editAnnouncement.id}`, { content: editAnnouncement.content })
            .then(response => {
                setAnnouncements(announcements.map(announcement => 
                    announcement.id === editAnnouncement.id ? response.data.announcement : announcement
                ));
                setEditAnnouncement({ id: null, content: "" });
            })
            .catch(error => console.error("Error updating announcement:", error));
    };

    return (
        <div className="page">
            <h1>管理公告</h1>
            <div className="add-announcement">
                <textarea
                    value={newAnnouncement}
                    onChange={(e) => setNewAnnouncement(e.target.value)}
                    placeholder="輸入新公告內容"
                />
                <button onClick={handleAddAnnouncement}>新增公告</button>
            </div>
            <div className="announcement-list">
                {announcements.length > 0 ? (
                    announcements.map(announcement => (
                        <div key={announcement.id} className="announcement-item">
                            {editAnnouncement.id === announcement.id ? (
                                <div>
                                    <textarea
                                        value={editAnnouncement.content}
                                        onChange={(e) => setEditAnnouncement({ ...editAnnouncement, content: e.target.value })}
                                    />
                                    <button onClick={handleUpdateAnnouncement}>更新公告</button>
                                    <button onClick={() => setEditAnnouncement({ id: null, content: "" })}>取消</button>
                                </div>
                            ) : (
                                <div>
                                    <p>{announcement.content}</p>
                                    <button onClick={() => handleEditAnnouncement(announcement.id, announcement.content)}>修改</button>
                                    <button onClick={() => handleDeleteAnnouncement(announcement.id)}>刪除</button>
                                </div>
                            )}
                        </div>
                    ))
                ) : (
                    <p>目前沒有公告。</p>
                )}
            </div>
        </div>
    );
};

export default ManageAnnouncement;