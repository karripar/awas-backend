BEGIN TRANSACTION;
CREATE TABLE posts (
            post_id TEXT PRIMARY KEY,
            user_id TEXT NOT NULL,
            title TEXT NOT NULL,
            text TEXT NOT NULL,
            private BOOLEAN DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (user_id)
        );
INSERT INTO "posts" VALUES('76c223ed-780e-4acf-9aea-2e8553a2e798','06e21a83-e950-4896-ba66-518525280b8d','Assignment scope','Review login, feed browsing, and admin actions for the demo.',0,'2026-05-31 16:30:04');
INSERT INTO "posts" VALUES('e04d551b-d0ae-4a4f-a820-d03b6384f35b','75a12e63-e55f-4100-b253-1ab5305c2f9c','Private notes','This entry should only be visible to trusted users in the real app.',1,'2026-05-31 16:30:04');
INSERT INTO "posts" VALUES('b865892f-a7ab-4417-9a7d-a5ad28481c65','5ad89ff1-855c-42da-84d6-159438bab284','Review checklist','The report should mention the attack surface and the intended weak points.',1,'2026-05-31 16:30:04');
INSERT INTO "posts" VALUES('298358fb-c258-4d7e-bade-ce300218b057','2fd71e2b-c972-49b2-8d81-468c7f915ae3','Public announcement','This is a public post that anyone can see.',0,'2026-05-31 16:30:04');
INSERT INTO "posts" VALUES('7d023369-c6a8-4b05-b749-6b9a704690b4','06e21a83-e950-4896-ba66-518525280b8d','Demo feedback','The demo was well-structured and covered the key points.',0,'2026-05-31 16:30:04');
INSERT INTO "posts" VALUES('8d290ab4-ad44-4cc4-98b9-7ec6d8dfa175','75a12e63-e55f-4100-b253-1ab5305c2f9c','Security tips','Always use strong passwords and enable 2FA.',0,'2026-05-31 16:30:04');
INSERT INTO "posts" VALUES('a8f595d6-616f-4a7c-8d8f-b7cbb9293d81','8127cc1d-f2d0-410c-8ca4-3bd0830470ea','title','this is my first post',0,'2026-05-31 16:32:17');
CREATE TABLE users (
            user_id TEXT PRIMARY KEY,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            email TEXT NOT NULL,
            role TEXT DEFAULT 'user',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
INSERT INTO "users" VALUES('5ad89ff1-855c-42da-84d6-159438bab284','admin_7f3a91','0192023a7bbd73250516f069df18b500','admin@awas.local','user','2026-05-31 16:30:04');
INSERT INTO "users" VALUES('06e21a83-e950-4896-ba66-518525280b8d','joel','62cc2d8b4bf2d8728120d052163a77df','joel@awas.local','user','2026-05-31 16:30:04');
INSERT INTO "users" VALUES('75a12e63-e55f-4100-b253-1ab5305c2f9c','samu','62cc2d8b4bf2d8728120d052163a77df','samu@awas.local','user','2026-05-31 16:30:04');
INSERT INTO "users" VALUES('2fd71e2b-c972-49b2-8d81-468c7f915ae3','karri','62cc2d8b4bf2d8728120d052163a77df','karri@awas.local','user','2026-05-31 16:30:04');
INSERT INTO "users" VALUES('8127cc1d-f2d0-410c-8ca4-3bd0830470ea','karripar','e7e941b1f09f266540c6780db51d5f58','karripar@metropolia.fi','admin','2026-05-31 16:31:16');
COMMIT;
