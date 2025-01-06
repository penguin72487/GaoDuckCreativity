import React, { useState, useEffect } from "react";
import axios from "axios";

const RatingCard = ({ tid }) => {
    const [scores, setScores] = useState({ creativity: 0, usability: 0, design: 0, completeness: 0 });
    const [submitted, setSubmitted] = useState(false);
    const [currentUser, setCurrentUser] = useState(null); // 用於存儲用戶信息
    const [loading, setLoading] = useState(true); // 用於控制加載狀態

    // 在組件加載時獲取用戶數據
    useEffect(() => {
        const token = localStorage.getItem("authToken");
        if (token) {
            axios
                .get("http://127.0.0.1:5000/api/auth/protected", {
                    headers: { Authorization: `Bearer ${token}` },
                })
                .then((response) => {
                    const userData = response.data.data;
                    setCurrentUser({
                        id: userData.u_id,
                        userId: userData.ID_num,
                        role: userData.role,
                    });
                })
                .catch((error) => {
                    console.error("Failed to fetch user data:", error);
                    setCurrentUser(null);
                })
                .finally(() => setLoading(false));
        } else {
            setLoading(false);
        }
    }, []);

    const handleScoreChange = (category, value) => {
        setScores({ ...scores, [category]: value });
    };

    const handleSubmit = (e) => {
        e.preventDefault();

        // 確保用戶數據已加載且有效
        if (!currentUser || !currentUser.id || !currentUser.userId) {
            console.error("currentUser, id, or userId is undefined");
            alert("使用者未登入或必要資料缺失！");
            return;
        }

        const payload = {
            tid,
            u_id: currentUser.id,
            ID_num: currentUser.userId,
            ...scores,
        };

        console.log("Submitting payload:", payload);

        axios
            .post("http://127.0.0.1:5000/api/projects/score", payload)
            .then((response) => {
                alert(response.data.message);
                setScores({ creativity: 0, usability: 0, design: 0, completeness: 0 });
                setSubmitted(true);
                // 提交後刷新頁面
                window.location.reload();
            })
            .catch((error) => {
                console.error("Error submitting scores:", error);
                alert("提交評分失敗，請稍後再試！");
            });
    };

    const renderDots = (category, currentValue) => {
        return Array.from({ length: 10 }, (_, idx) => (
            <span
                key={idx + 1}
                onClick={() => handleScoreChange(category, idx + 1)}
                style={{
                    cursor: "pointer",
                    margin: "0 5px",
                    color: idx + 1 <= currentValue ? "#f39c12" : "#ccc",
                    fontSize: "24px",
                }}
            >
                ●
            </span>
        ));
    };

    // 顯示加載提示
    if (loading) {
        return <div>Loading user data...</div>;
    }

    return (
        <div>
            <form onSubmit={handleSubmit}>
                <div>
                    <label>創意性 (1-10)</label>
                    <div>{renderDots("creativity", scores.creativity)}</div>
                </div>

                <div>
                    <label>實用性 (1-10)</label>
                    <div>{renderDots("usability", scores.usability)}</div>
                </div>

                <div>
                    <label>美觀度 (1-10)</label>
                    <div>{renderDots("design", scores.design)}</div>
                </div>

                <div>
                    <label>完整度 (1-10)</label>
                    <div>{renderDots("completeness", scores.completeness)}</div>
                </div>

                <button type="submit" disabled={submitted}>
                    {submitted ? "已提交" : "提交評分"}
                </button>
            </form>
        </div>
    );
};

export default RatingCard;
