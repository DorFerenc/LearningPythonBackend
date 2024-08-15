db.createUser(
    {
        user:"admin",
        pwd:"password",
        roles: [
            { role: "readWrite", db:"firstdb" },
            { role: "root", db: "admin" },
            { role: "userAdminAnyDatabase", db: "admin" },
            { role: "dbAdminAnyDatabase", db: "admin" },
            { role: "readWriteAnyDatabase", db: "admin" }
        ]
    }
)