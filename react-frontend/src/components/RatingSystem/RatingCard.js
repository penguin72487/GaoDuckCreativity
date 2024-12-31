import React, { useState } from "react";
import axios from "axios";

const RatingCard = ({ tid }) => {
    const [scores, setScores] = useState({ creativity: 0, usability: 0, design: 0, completeness: 0 });
    const [submitted, setSubmitted] = useState(false);

    const handleScoreChange = (category, value) => {
        setScores({ ...scores, [category]: value });
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        const payload = { tid, ...scores };
        axios
            .post("http://127.0.0.1:5000/api/projects/score", payload)
            .then(response => {
                alert(response.data.message);
                setScores({ creativity: 0, usability: 0, design: 0, completeness: 0 });
                setSubmitted(true); // 標記為已評分
            })
            .catch(error => {
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
                    fontSize: "24px"
                }}
            >
                ●
            </span>
        ));
    };

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
