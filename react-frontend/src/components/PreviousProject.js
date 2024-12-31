import React from "react";

const PreviousProjects = () => {
    return (
        <div className="page">
            <h1>歷屆作品檢視</h1>
            <form>
                <label>年份</label>
                <select>
                    <option>2024</option>
                    <option>2023</option>
                </select>
                <label>關鍵字搜尋</label>
                <input type="text" />

                <button type="submit">搜尋</button>
            </form>
        </div>
    );
};

export default PreviousProjects;
