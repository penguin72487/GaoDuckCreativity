import React from "react";
import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";
import Home from "./components/Home";
import Announcement from "./components/Announcement";
import AccountManagement from "./components/AccountManagement/AccountManagement";
import RegisterAccount from "./components/RegisterAccount";
import EnrollForm from "./components/EnrollForm";
import WorkList from "./components/WorkList";
import ScoringSystem from "./components/ScoringSystem";
import PreviousWorks from "./components/PreviousWorks";
import Login from "./components/Login";
import "./App.css";

function App() {
    return (
        <Router>
            <div className="App">
                <header>高雄大學激發學生創意競賽管理系統</header>
                <div className="container">
                    {/* 側邊欄 */}
                    <nav className="sidebar">
                        <ul>
                            <li><Link to="/">首頁</Link></li>
                            <li><Link to="/account-management">帳號管理</Link></li>
                            <li><Link to="/register-account">註冊帳號</Link></li>
                            <li><Link to="/enroll-form">報名表單</Link></li>
                            <li><Link to="/work-list">作品列表</Link></li>
                            <li><Link to="/scoring-system">評分系統</Link></li>
                            <li><Link to="/previous-works">歷屆作品檢視</Link></li>
                        </ul>

                        {/* 左下角固定的登入按鈕 */}
                        <div className="sidebar-bottom">
                            <Link to="/login">登入</Link>
                        </div>
                    </nav>


                    {/* 主要內容 */}
                    <div className="main-content">
                        <Routes>
                            <Route path="/" element={<Home />} />
                            <Route path="/announcement" element={<Announcement />} />
                            <Route path="/account-management" element={<AccountManagement />} />
                            <Route path="/register-account" element={<RegisterAccount />} />
                            <Route path="/enroll-form" element={<EnrollForm />} />
                            <Route path="/work-list" element={<WorkList />} />
                            <Route path="/scoring-system" element={<ScoringSystem />} />
                            <Route path="/previous-works" element={<PreviousWorks />} />
                            <Route path="/login" element={<Login />} />
                        </Routes>
                    </div>
                </div>
            </div>
        </Router>
    );
}

export default App;
