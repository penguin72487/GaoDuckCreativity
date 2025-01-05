import React, { useState, useEffect } from "react";
import axios from "axios";
import "./ManageAnnouncement.css";

const ManageAnnouncement = ({ currentUser }) => {
    const [announcements, setAnnouncements] = useState([]); // 初始化為空數組
    const [newAnnouncement, setNewAnnouncement] = useState({ title: "", content: "" });
    const [editAnnouncement, setEditAnnouncement] = useState({ id: null, title: "", content: "" });
    const [message, setMessage] = useState("");

    useEffect(() => {
        axios.get("http://127.0.0.1:5000/api/announcements")
            .then(response => {
                console.log("API 回傳的公告:", response.data);
                if (Array.isArray(response.data.announcements)) {
                    setAnnouncements(response.data.announcements);
                } else {
                    console.error("API 回傳的格式錯誤:", response.data);
                    setAnnouncements([]);
                }
            })
            .catch(error => console.error("Error fetching announcements:", error));
    }, []);
    
    
    const handleAddAnnouncement = () => {
        if (!newAnnouncement.title.trim() || !newAnnouncement.content.trim()) {
            alert("公告標題和內容不能為空！");
            return;
        }

        if (!currentUser || !currentUser.id) {
            alert("使用者未登入或使用者 ID 無效！");
            return;
        }

        axios.post("http://127.0.0.1:5000/api/announcements", { title: newAnnouncement.title, content: newAnnouncement.content, publisher_u_id: currentUser.id }) // 使用當前使用者的 ID
            .then(response => {
                setAnnouncements([...announcements, response.data.announcement]);
                setNewAnnouncement({ title: "", content: "" });
                setMessage("公告新增成功！");
            })
            .catch(error => {
                console.error("Error adding announcement:", error);
                setMessage("公告新增失敗！");
            });
    };

    const handleDeleteAnnouncement = (id) => {
        axios.delete(`http://127.0.0.1:5000/api/announcements/${id}`)
            .then(() => {
                setAnnouncements(announcements.filter(announcement => announcement.id !== id));
                setMessage("公告刪除成功！");
            })
            .catch(error => {
                console.error("Error deleting announcement:", error);
                setMessage("公告刪除失敗！");
            });
    };

    const handleEditAnnouncement = (id, title, content) => {
        setEditAnnouncement({ id, title, content });
    };

    const handleUpdateAnnouncement = () => {
        if (!editAnnouncement.title || !editAnnouncement.content) {
            alert("公告標題和內容不能為空！");
            return;
        }

        if (!editAnnouncement.title.trim() || !editAnnouncement.content.trim()) {
            alert("公告標題和內容不能為空！");
            return;
        }

        if (!currentUser || !currentUser.id) {
            alert("使用者未登入或使用者 ID 無效！");
            return;
        }

        axios.put(`http://127.0.0.1:5000/api/announcements/${editAnnouncement.id}`, { title: editAnnouncement.title, content: editAnnouncement.content, publisher_u_id: currentUser.id }) // 使用當前使用者的 ID
            .then(response => {
                setAnnouncements(announcements.map(announcement => 
                    announcement.id === editAnnouncement.id ? response.data.announcement : announcement
                ));
                setEditAnnouncement({ id: null, title: "", content: "" });
                setMessage("公告更新成功！");
            })
            .catch(error => {
                console.error("Error updating announcement:", error);
                setMessage("公告更新失敗！");
            });
    };

    return (
        <div className="page">
            <h1>管理公告</h1>
            {message && <p className="message">{message}</p>}
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
                                    <div className="button-group">
                                        <button onClick={handleUpdateAnnouncement}>更新公告</button>
                                        <button onClick={() => setEditAnnouncement({ id: null, title: "", content: "" })}>取消</button>
                                    </div>
                                </div>
                            ) : (
                                <div>
                                    <h3>{announcement.title}</h3>
                                    <p>{announcement.content}</p>
                                    <p>發布時間: {announcement.publish_timestamp}</p>
                                    <p>最後更新時間: {announcement.last_update_timestamp}</p>
                                    <div className="button-group">
                                        <button onClick={() => handleEditAnnouncement(announcement.id, announcement.title, announcement.content)}>修改</button>
                                        <button onClick={() => handleDeleteAnnouncement(announcement.id)}>刪除</button>
                                    </div>
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