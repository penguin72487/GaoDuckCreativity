import React, { useEffect, useState } from "react";
import axios from "axios";

const AccountManagement = () => {
    const [accounts, setAccounts] = useState([]);

    useEffect(() => {
        axios.get("http://127.0.0.1:5000/api/accounts")
            .then(response => setAccounts(response.data.accounts))
            .catch(error => console.error("Error fetching accounts:", error));
    }, []);

    return (
        <div className="page">
            <h1>帳號管理</h1>
            <table>
                <thead>
                    <tr>
                        <th>姓名</th>
                        <th>學號</th>
                        <th>Email</th>
                        <th>類別</th>
                        <th>操作</th>
                    </tr>
                </thead>
                <tbody>
                    {accounts.map((account, index) => (
                        <tr key={index}>
                            <td>{account.name}</td>
                            <td>{account.student_id}</td>
                            <td>{account.email}</td>
                            <td>{account.role}</td>
                            <td>
                                <button>編輯</button> | <button>停用</button>
                            </td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
};

export default AccountManagement;
