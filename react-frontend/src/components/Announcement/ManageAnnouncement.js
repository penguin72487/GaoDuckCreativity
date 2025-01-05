import React, { useState, useEffect } from "react";
import axios from "axios";
import "./ManageAnnouncement.css";

const ManageAnnouncement = () => {
    const [announcements, setAnnouncements] = useState([]); // 初始化為空數組
    const [newAnnouncement, setNewAnnouncement] = useState({ title: "", content: "" });
    const [editAnnouncement, setEditAnnouncement] = useState({ id: null, title: "", content: "" });

    useEffect(() => {
        // 獲取現有公告
        axios.get("http://127.0.0.1:5000/api/announcements")
            .then(response => setAnnouncements(response.data.announcements || [])) // 確保是數組
            .catch(error => console.error("Error fetching announcements:", error));
    }, []);

    const handleAddAnnouncement = () => {
        if (!newAnnouncement.title.trim() || !newAnnouncement.content.trim()) {
            alert("公告標題和內容不能為空！");
            return;
        }

        axios.post("http://127.0.0.1:5000/api/announcements", { title: newAnnouncement.title, content: newAnnouncement.content })
            .then(response => {
                setAnnouncements([...announcements, response.data.announcement]);
                setNewAnnouncement({ title: "", content: "" });
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

    const handleEditAnnouncement = (id, title, content) => {
        setEditAnnouncement({ id, title, content });
    };

    const handleUpdateAnnouncement = () => {
        if (!editAnnouncement.title.trim() || !editAnnouncement.content.trim()) {
            alert("公告標題和內容不能為空！");
            return;
        }

        axios.put(`http://127.0.0.1:5000/api/announcements/${editAnnouncement.id}`, { title: editAnnouncement.title, content: editAnnouncement.content })
            .then(response => {
                setAnnouncements(announcements.map(announcement => 
                    announcement.id === editAnnouncement.id ? response.data.announcement : announcement
                ));
                setEditAnnouncement({ id: null, title: "", content: "" });
            })
            .catch(error => console.error("Error updating announcement:", error));
    };

    return (
        <div className="page">
            <h1>管理公告</h1>
            <div className="add-announcement">
                <input
                    type="text"
                    value={newAnnouncement.title}
                    onChange={(e) => setNewAnnouncement({ ...newAnnouncement, title: e.target.value })}
                    placeholder="輸入公告標題"
                />
                <textarea
                    value={newAnnouncement.content}
                    onChange={(e) => setNewAnnouncement({ ...newAnnouncement, content: e.target.value })}
                    placeholder="輸入公告內容"
                />
                <button onClick={handleAddAnnouncement}>新增公告</button>
            </div>
            <div className="announcement-list">
                {announcements.length > 0 ? (
                    announcements.map(announcement => (
                        <div key={announcement.id} className="announcement-item">
                            {editAnnouncement.id === announcement.id ? (
                                <div>
                                    <input
                                        type="text"
                                        value={editAnnouncement.title}
                                        onChange={(e) => setEditAnnouncement({ ...editAnnouncement, title: e.target.value })}
                                        placeholder="輸入公告標題"
                                    />
                                    <textarea
                                        value={editAnnouncement.content}
                                        onChange={(e) => setEditAnnouncement({ ...editAnnouncement, content: e.target.value })}
                                        placeholder="輸入公告內容"
                                    />
                                    <button onClick={handleUpdateAnnouncement}>更新公告</button>
                                    <button onClick={() => setEditAnnouncement({ id: null, title: "", content: "" })}>取消</button>
                                </div>
                            ) : (
                                <div>
                                    <h3>{announcement.title}</h3>
                                    <p>{announcement.content}</p>
                                    <p>發布時間: {announcement.publish_timestamp}</p>
                                    <p>最後更新時間: {announcement.last_update_timestamp}</p>
                                    <button onClick={() => handleEditAnnouncement(announcement.id, announcement.title, announcement.content)}>修改</button>
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