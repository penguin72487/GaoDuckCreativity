import React, { useState, useEffect } from "react";
import { BrowserRouter as Router, Routes, Route, Link, Navigate } from "react-router-dom";
import Home from "./components/Home";
import Announcement from "./components/Announcement";
import AccountManagement from "./components/AccountManagement/AccountManagement";
import RegisterAccount from "./components/RegisterAccount";
import EnrollForm from "./components/EnrollForm";
import ProjectList from "./components/ProjectList";
import RatingSystem from "./components/RatingSystem/RatingSystem";
import PreviousProject from "./components/PreviousProject";
import Login from "./components/Login";
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
                        setUserId(response.data.data.student_id);
                    })
                    .catch(() => {
                        setIsAuthenticated(false);
                        setUserRole("");
                        setUserId("");
                    });
            }
        }, 1000); // 每5秒檢查一次
    
        return () => clearInterval(interval); // 清理定時器
    }, []);
    

    const handleLogout = () => {
        localStorage.removeItem("authToken"); // 清除令牌
        setIsAuthenticated(false); // 更新狀態
        setUserRole("");
        setUserId("");
        console.log("已登出");
    };

    return (
        <Router>
            <div className="App">
                <header>高雄大學激發學生創意競賽管理系統</header>
                <div className="container">
                    {/* 側邊欄 */}
                    <nav className="sidebar">
                        <ul>
                            <li><Link to="/">首頁</Link></li>
                            {userRole === "admin" && (
                                <li><Link to="/account-management">帳號管理</Link></li>
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
                        </Routes>
                    </div>
                </div>
            </div>
        </Router>
    );
}

export default App;
