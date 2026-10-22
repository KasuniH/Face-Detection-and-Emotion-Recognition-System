import hashlib
import streamlit as st

# In production, store salted hashes in a secure database
USERS_DB = {
    "admin": hashlib.sha256("AdminPassword123!".encode()).hexdigest(),
    "manager": hashlib.sha256("ManagerPass2026!".encode()).hexdigest(),
}


class AuthManager:

  @staticmethod
  def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

  @classmethod
  def authenticate_user(cls, username, password) -> bool:
    if username in USERS_DB:
      return USERS_DB[username] == cls.hash_password(password)
    return False

  @staticmethod
  def render_login_form():
    """Renders login UI in Streamlit sidebar."""
    if "authenticated" not in st.session_state:
      st.session_state["authenticated"] = False
      st.session_state["username"] = ""

    if not st.session_state["authenticated"]:
      st.sidebar.subheader("🔒 Admin Login Required")
      user = st.sidebar.text_input("Username")
      pwd = st.sidebar.text_input("Password", type="password")

      if st.sidebar.button("Login"):
        if AuthManager.authenticate_user(user, pwd):
          st.session_state["authenticated"] = True
          st.session_state["username"] = user
          st.sidebar.success(f"Logged in as {user}")
          st.rerun()
        else:
          st.sidebar.error("Invalid Username or Password")
    else:
      st.sidebar.write(f"👤 Logged in: **{st.session_state['username']}**")
      if st.sidebar.button("Logout"):
        st.session_state["authenticated"] = False
        st.session_state["username"] = ""
        st.rerun()
