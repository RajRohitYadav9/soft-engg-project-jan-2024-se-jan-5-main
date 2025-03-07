class Auth(db.Model):
    __tablename__ = "auth"
    id = db.Column(db.String, primary_key=True)
    role = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    web_token = db.Column(db.String, unique=True, nullable=True)
    is_verified = db.Column(db.Boolean, default=False, nullable=False)
    is_logged = db.Column(db.Boolean, default=False, nullable=False)
    token_created_on = db.Column(
        db.Integer, nullable=True, default=0
    )  # time is stored as a timestamp
    token_expiry_on = db.Column(db.Integer, nullable=True, default=0)
    name = db.Column(db.String, nullable=False)
    username = db.Column(db.String, nullable=False)
    profile_photo_loc = db.Column(db.String, default="", nullable=True)

    def __repr__(self):
        return f"Auth object for: {self.user_id} | {self.role} | {self.name}"

class Ticket(db.Model):
    __tablename__ = "ticket"
    ticket_id = db.Column(db.String, primary_key=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=True, default="")
    ticket_discourse_post_id = db.Column(db.Integer, nullable=False)
    is_solved = db.Column(db.Boolean, default=False)
    solution_id = db.Column(db.Integer, nullable=True, foreign_keys=db.ForeignKey("ticket_solution.id"))
    priority = db.Column(
        db.String, nullable=False, default="low"
    )  # low (default), medium, high
    tag_1 = db.Column(db.String, nullable=False)
    tag_2 = db.Column(db.String, nullable=True, default="")
    tag_3 = db.Column(db.String, nullable=True, default="")
    status = db.Column(db.String, nullable=False, default="pending")  # pending/resolved
    votes = db.Column(
        db.Integer, nullable=False, default=0
    )  # creater can't vote, 1 vote/student
    created_by = db.Column(db.String, nullable=False)
    created_on = db.Column(
        db.Integer, nullable=False, default=0
    )  # time is stored as a timestamp

    def __repr__(self):
        return f"Ticket object for: {self.ticket_id} | {self.title}"



class TicketSolution(db.Model):
    __tablename__ = 'ticket_solution'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String, nullable=False)
    resolved_by = db.Column(db.String, nullable=False) ## Let's store the username of the resolved.
    resolved_on = db.Column(
        db.Integer, nullable=True, default=0
    )  # time is stored as a timestamp



class TicketAttachment(db.Model):
    __tablename__ = "ticketattachment"
    ticket_id = db.Column(
        db.String, db.ForeignKey("ticket.ticket_id"), primary_key=True
    )
    user_id = db.Column(db.String, db.ForeignKey("auth.id"), primary_key=True)
    attachment_loc = db.Column(db.String, nullable=False, primary_key=True)

    def __repr__(self):
        return f"TicketAttachment object for: {self.ticket_id}"


class TicketVote(db.Model):
    __tablename__ = "ticketvote"
    ticket_id = db.Column(
        db.String, db.ForeignKey("ticket.ticket_id"), primary_key=True
    )
    user_id = db.Column(db.String, db.ForeignKey("auth.id"), primary_key=True)

    def __repr__(self):
        return f"TicketVote object for: {self.ticket_id}"


class FAQ(db.Model):
    __tablename__ = "faq"
    faq_id = db.Column(db.String, primary_key=True)
    question = db.Column(db.String, nullable=False)
    solution = db.Column(db.String, nullable=False)
    tag_1 = db.Column(db.String, nullable=False)
    tag_2 = db.Column(db.String, nullable=True, default="")
    tag_3 = db.Column(db.String, nullable=True, default="")
    created_by = db.Column(db.String, nullable=False)

    def __repr__(self):
        return f"FAQ object for: {self.FAQ_id}"


class FAQAttachment(db.Model):
    __tablename__ = "faqattachment"
    faq_id = db.Column(db.String, db.ForeignKey("faq.faq_id"), primary_key=True)
    attachment_loc = db.Column(db.String, nullable=False, primary_key=True)

    def __repr__(self):
        return f"FAQAttachment object for: {self.faq_id}"