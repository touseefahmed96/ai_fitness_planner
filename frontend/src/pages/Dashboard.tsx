import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

function Dashboard() {
    const navigate = useNavigate();
    const [user, setUser] = useState<any>(null);
    const [loading, setLoading] = useState(true);

    const handleLogout = () => {
        localStorage.removeItem("token");
        navigate("/login");
    };

    useEffect(() => {
        const token = localStorage.getItem("token");

        if (!token) {
            navigate("/login");
        } else {
            fetch("http://localhost:8000/api/v1/user/me", {
                headers: {
                    "Authorization": `Bearer ${token}`,
                },
            })
                .then((response) => response.json())
                .then((data) => {
                    setUser(data);
                    setLoading(false);
                })
                .catch(() => {
                    setLoading(false);
                });
        }
    }, [navigate]);

    if (loading) {
        return <div>Loading...</div>;
    }

    return (
        <div className="dashboard-container">
            <h2>Welcome, {user?.name}!</h2>
            <p>Your goal: {user?.goal}</p>
            <div className="dashboard-buttons">
                <button onClick={() => navigate("/diet")}>View Diet Plan</button>
                <button onClick={() => navigate("/workout")}>View Workout Plan</button>
                <button className="logout-btn" onClick={handleLogout}>
                    Logout
                </button>
            </div>
        </div>
    );
}

export default Dashboard;
