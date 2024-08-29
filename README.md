# Bot Quiz Discord

Simple Quiz Bot for Discord

#Indonesia

Quiz Bot
Quiz Bot adalah bot Discord yang dirancang untuk mengadakan kuis interaktif dengan fitur leaderboard, poin, dan badge. Bot ini dapat digunakan untuk menguji pengetahuan pengguna di server Discord dengan cara yang menyenangkan dan kompetitif.

Cara Menggunakan

- Tambahkan Bot ke Server Discord: Undang bot ke server Discord yang kamu kelola.

- Tetapkan Role:
  ~ Pastikan pengguna yang akan mengelola kuis memiliki peran "guru". Role ini diperlukan untuk menjalankan perintah seperti menambahkan pertanyaan dan memulai kuis.

  ~ Pengguna lainnya yang akan mengikuti kuis harus memiliki peran "siswa".

- Mulai Kuis: Gunakan perintah !start_quiz untuk memulai kuis. Hanya pengguna dengan peran "guru" yang dapat menjalankan perintah ini.

- Tambahkan Pertanyaan: Gunakan perintah !add_question untuk menambahkan pertanyaan baru ke dalam kuis. Hanya pengguna dengan peran "guru" yang dapat menambahkan pertanyaan.

- Lihat Leaderboard: Gunakan perintah !leaderboard untuk melihat peringkat pengguna berdasarkan skor kuis.

- Klaim Badge: Gunakan perintah !claim_badge jika kamu berada di peringkat 3 teratas untuk mendapatkan badge. Hanya pengguna dengan peran "siswa" yang dapat mengklaim badge.

- Cek Izin: Gunakan perintah !check_permissions untuk memeriksa izin yang dimiliki bot di server. Perintah ini hanya dapat dijalankan oleh pengguna dengan izin administrator.

Commands

- !start_quiz
  Mulai kuis dengan pertanyaan acak yang telah ditambahkan. Hanya pengguna dengan peran "guru" yang dapat menjalankan perintah ini.

- !add_question <pertanyaan> | <jawaban_benar> | <jawaban_salah1> | <jawaban_salah2> | ...
  Tambahkan pertanyaan baru ke dalam kuis. Setiap pertanyaan harus memiliki satu jawaban benar dan setidaknya satu jawaban salah. Perintah ini hanya bisa digunakan oleh pengguna dengan peran "guru".

- !leaderboard
  Menampilkan leaderboard yang menunjukkan peringkat pengguna berdasarkan skor kuis.

- !claim_badge
  Klaim badge untuk pengguna yang berada di peringkat 3 teratas. Badge akan ditambahkan ke nama panggilan pengguna di server. Hanya pengguna dengan peran "siswa" yang dapat mengklaim badge.

- !check_permissions
  Periksa izin yang dimiliki bot di server. Hanya pengguna dengan izin administrator yang dapat menggunakan perintah ini.

#English

Quiz Bot
Quiz Bot is a Discord bot designed to host interactive quizzes with leaderboard, points, and badge features. This bot can be used to test users' knowledge on a Discord server in a fun and competitive way.

How to Use

- Add the Bot to Your Discord Server: Invite the bot to the Discord server you manage.

- Assign Roles:
  ~ Ensure that users who will manage the quiz have the "guru" role. This role is required to execute commands like adding questions and starting the quiz.

  ~ Other users who will participate in the quiz should have the "siswa" role.

- Start the Quiz: Use the !start_quiz command to start the quiz. Only users with the "guru" role can run this command.

- Add Questions: Use the !add_question command to add new questions to the quiz. Only users with the "guru" role can add questions.

- View the Leaderboard: Use the !leaderboard command to view the user rankings based on quiz scores.

- Claim a Badge: Use the !claim_badge command if you are in the top 3 to claim your badge. Only users with the "siswa" role can claim badges.

- Check Permissions: Use the !check_permissions command to check the bot’s permissions on the server. This command can only be run by users with administrator permissions.

Commands

- !start_quiz
  Start the quiz with random questions that have been added. Only users with the "guru" role can run this command.

- !add_question <question> | <correct_answer> | <wrong_answer1> | <wrong_answer2> | ...
  Add a new question to the quiz. Each question must have one correct answer and at least one wrong answer. This command can only be used by users with the "guru" role.

- !leaderboard
  Displays the leaderboard showing the rankings of users based on quiz scores.

- !claim_badge
  Claim a badge for users who are in the top 3. The badge will be added to the user’s nickname on the server. Only users with the "siswa" role can claim badges.

- !check_permissions
  Check the bot's permissions on the server. Only users with administrator permissions can use this command.
