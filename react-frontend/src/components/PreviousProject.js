import React, { useEffect, useState } from "react";
import axios from "axios";
import ProjectCard from "./ProjectCard/ProjectCard";

const PreviousProjects = () => {
    const [projects, setProjects] = useState([]);
    const [year, setYear] = useState("2024");
    const [keyword, setKeyword] = useState("");

    const fetchProjectsByYear = (selectedYear) => {
        axios
            .get(`http://127.0.0.1:5000/api/projects/list/${selectedYear}`)
            .then(response => setProjects(response.data.projects))
            .catch(error => {
                console.error("Error fetching projects:", error);
                alert("無法獲取歷屆作品列表，請稍後再試！");
            });
    };

    useEffect(() => {
        fetchProjectsByYear(year);
    }, [year]);

    const handleFilter = (e) => {
        e.preventDefault();
        const filtered = projects.filter(project =>
            keyword === "" || project.name.includes(keyword)
        );
        setProjects(filtered);
    };

    return (
        <div className="page">
            <h1>歷屆作品檢視</h1>
            <form onSubmit={handleFilter}>
                <label>年份</label>
                <select value={year} onChange={(e) => setYear(e.target.value)}>
                    <option>2025</option>
                    <option>2024</option>
                    <option>2023</option>
                </select>
                <label>關鍵字搜尋</label>
                <input
                    type="text"
                    value={keyword}
                    onChange={(e) => setKeyword(e.target.value)}
                />
                <button type="submit">搜尋</button>
            </form>

            <div style={{ marginTop: "2rem" }}>
                <h2>搜尋結果</h2>
                {projects.length > 0 ? (
                    projects.map(project => (
                        <ProjectCard key={project.tid} project={project} />
                    ))
                ) : (
                    <p>未找到相關作品。</p>
                )}
            </div>
        </div>
    );
};

export default PreviousProjects;
