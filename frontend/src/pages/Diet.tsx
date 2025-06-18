import React, { useEffect, useState } from "react";

function Diet() {
    const [userId, setUserId] = useState<number | null>(null);
    const [calories, setCalories] = useState<number | string>("");  // Default to empty string
    const [dietPlan, setDietPlan] = useState<string | null>(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    // Fetch user information and set userId
    useEffect(() => {
        const token = localStorage.getItem("token");

        if (!token) {
            window.location.href = "/login";  // Redirect to login if no token
        } else {
            // Fetch user info to get the user_id
            fetch("http://localhost:8000/api/v1/user/me", {
                headers: {
                    "Authorization": `Bearer ${token}`,
                },
            })
                .then((response) => response.json())
                .then((data) => {
                    setUserId(data.id);  // Set user_id from the backend response
                    setLoading(false);
                })
                .catch(() => {
                    setError("Failed to fetch user data");
                    setLoading(false);
                });
        }
    }, []);

    // Fetch diet plan when user submits calories
    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();

        if (userId && calories) {
            setLoading(true);
            setError(null);

            // Fetch diet plan from the backend
            fetch("http://localhost:8000/api/v1/diet/generate", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": `Bearer ${localStorage.getItem("token")}`,
                },
                body: JSON.stringify({
                    user_id: userId,  // Pass the user_id
                    calories: parseInt(calories as string, 10),  // Pass the calories as number
                }),
            })
                .then((response) => response.json())
                .then((data) => {
                    setDietPlan(data.diet_plan);
                    setLoading(false);
                })
                .catch(() => {
                    setError("Failed to load diet plan");
                    setLoading(false);
                });
        } else {
            setError("Please provide valid input.");
        }
    };

    if (loading) {
        return <div>Loading your diet plan...</div>;
    }

    if (error) {
        return <div>{error}</div>;
    }

    return (
        <div className="form-container">
            <h2>Your Diet Plan</h2>

            {dietPlan ? (
                <div>
                    <h3>Your Personalized Diet Plan:</h3>
                    <p>{dietPlan}</p>
                </div>
            ) : (
                <form onSubmit={handleSubmit}>
                    <div>
                        <label htmlFor="calories">Enter your daily calorie intake:</label>
                        <input
                            type="number"
                            id="calories"
                            placeholder="Calories"
                            value={calories}
                            onChange={(e) => setCalories(e.target.value)}
                            required
                        />
                    </div>

                    <button type="submit">Generate Diet Plan</button>
                </form>
            )}
        </div>
    );
}

export default Diet;
