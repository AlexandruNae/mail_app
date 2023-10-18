SELECT
    user.email,
    subscription.start_date,
    subscription.current_chunk,
    subscription.is_active,
    lecture.title
FROM
    subscription
JOIN
    user ON subscription.id_user = user.id
JOIN
    lecture ON subscription.id_lecture = lecture.id;