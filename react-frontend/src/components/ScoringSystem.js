import React, { useState } from "react";

const ScoringSystem = () => {
    const [scores, setScores] = useState({ creativity: "", usability: "", design: "", completeness: "" });

    const handleChange = (e) => {
        setScores({ ...scores, [e.target.name]: e.target.value });
    };

    return (
        <div className="page">
            <h1>評分系統</h1>
            <form>
                <label>創意性 (1-10)</label>
                <input type="number" name="creativity" onChange={handleChange} />

                <label>實用性 (1-10)</label>
                <input type="number" name="usability" onChange={handleChange} />

                <label>美觀度 (1-10)</label>
                <input type="number" name="design" onChange={handleChange} />

                <label>完整度 (1-10)</label>
                <input type="number" name="completeness" onChange={handleChange} />

                <button type="submit">提交評分</button>
            </form>
        </div>
    );
};

export default ScoringSystem;
