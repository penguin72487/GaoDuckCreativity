import React, { useState, useEffect } from "react";
import { BrowserRouter as Router, Routes, Route, Link, Navigate } from "react-router-dom";
import Home from "./components/Home";
import Announcement from "./components/Announcement/Announcement";
import AnnouncementPage from "./components/Announcement/AnnouncementPage";
import AccountManagement from "./components/AccountManagement/AccountManagement";
import RegisterAccount from "./components/RegisterAccount";
import EnrollForm from "./components/EnrollForm";
import ProjectList from "./components/ProjectList";
import RatingSystem from "./components/RatingSystem/RatingSystem";
import PreviousProject from "./components/PreviousProject";
import Login from "./components/Login";
import ManageAnnouncement from "./components/Announcement/ManageAnnouncement"; // 確保導入 ManageAnnouncement 組件
import "./App.css";
import axios from "axios";

// 受保護路由組件
const ProtectedRoute = ({ children, isAuthenticated }) => {
    if (!isAuthenticated) {
        return <Navigate to="/login" />;
    }
    return children;
};

function App() {
    const [isAuthenticated, setIsAuthenticated] = useState(false);
    const [userRole, setUserRole] = useState(""); // 保存用戶角色
    const [userId, setUserId] = useState(""); // 保存用戶學號
    const [uId, setUId] = useState(""); // 保存用戶 u_id

    // 檢查登入狀態
    useEffect(() => {
        const interval = setInterval(() => {
            const token = localStorage.getItem("authToken");

            if (token) {
                axios
                    .get("http://127.0.0.1:5000/api/auth/protected", {
                        headers: { Authorization: `Bearer ${token}` },
                    })
                    .then((response) => {
                        setIsAuthenticated(true);
                        setUserRole(response.data.data.role);
                        setUserId(response.data.data.ID_num);
                        setUId(response.data.data.u_id); // 假設 u_id 是從後端獲取的數據之一
                    })
                    .catch(() => {
                        setIsAuthenticated(false);
                        setUserRole("");
                        setUserId("");
                        setUId("");
                    });
            }
        }, 1000); // 每秒檢查一次

        return () => clearInterval(interval); // 清理定時器
    }, []);

    const handleLogout = () => {
        localStorage.removeItem("authToken"); // 清除令牌
        setIsAuthenticated(false); // 更新狀態
        setUserRole("");
        setUserId("");
        setUId("");
        console.log("已登出");
    };

    const currentUser = { id: uId, role: userRole, userId: userId }; // 構建 currentUser 對象

    return (
        <Router>
            <div className="App">
                <header>高雄大學激發學生創意競賽管理系統</header>
                <div className="container">
                    {/* 側邊欄 */}
                    <nav className="sidebar">
                        <ul>
                            <li><Link to="/">首頁</Link></li>
                            <li><Link to="/announcements">最新公告</Link></li>
                            {userRole === "admin" && (
                                <>
                                    <li><Link to="/account-management">帳號管理</Link></li>
                                    <li><Link to="/manage-announcements">管理公告</Link></li>
                                </>
                            )}
                            {!isAuthenticated && (
                                <li><Link to="/register-account">註冊帳號</Link></li>
                            )}
                            {userRole !== "teacher" && (
                                <li><Link to="/enroll-form">報名表單</Link></li>
                            )}
                            <li><Link to="/project-list">作品列表</Link></li>
                            {isAuthenticated && userRole !== "student" && (
                                <li><Link to="/rating-system">評分系統</Link></li>
                            )}
                            <li><Link to="/previous-project">往屆作品</Link></li>
                        </ul>

                        {/* 左下角用戶信息與登出按鈕 */}
                        <div className="sidebar-bottom">
                            {isAuthenticated ? (
                                <div className="user-card">
                                    <p className="user-id"><strong>ID:</strong> {userId}</p>
                                    <p className="user-role"><strong>身份別:</strong> {userRole}</p>
                                    <p className="user-id"><strong>u_id:</strong> {uId}</p>
                                    <button className="logout-button" onClick={handleLogout}>登出</button>
                                </div>
                            ) : (
                                <Link className="login-link" to="/login">登入</Link>
                            )}
                        </div>
                    </nav>

                    {/* 主內容區域 */}
                    <div className="main-content">
                        <Routes>
                            <Route path="/" element={<Home />} />
                            <Route path="/announcement" element={<Announcement />} />
                            <Route path="/announcements" element={<AnnouncementPage />} />
                            <Route
                                path="/account-management"
                                element={
                                    <ProtectedRoute isAuthenticated={isAuthenticated && userRole === "admin"}>
                                        <AccountManagement />
                                    </ProtectedRoute>
                                }
                            />
                            <Route path="/register-account" element={<RegisterAccount />} />
                            <Route path="/enroll-form" element={<EnrollForm />} />
                            <Route path="/project-list" element={<ProjectList />} />
                            <Route
                                path="/rating-system"
                                element={
                                    <ProtectedRoute isAuthenticated={isAuthenticated && userRole !== "student"}>
                                        <RatingSystem />
                                    </ProtectedRoute>
                                }
                            />
                            <Route path="/previous-project" element={<PreviousProject />} />
                            <Route path="/login" element={<Login />} />
                            <Route
                                path="/manage-announcements"
                                element={
                                    <ProtectedRoute isAuthenticated={isAuthenticated && userRole === "admin"}>
                                        <ManageAnnouncement currentUser={currentUser} />
                                    </ProtectedRoute>
                                }
                            />
                        </Routes>
                    </div>
                </div>
            </div>
        </Router>
    );
}

export default App;