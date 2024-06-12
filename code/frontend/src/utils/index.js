// /* eslint-disable no-unused-vars */
export function show_error_and_logout(state,message) {
    state.$flashMessage.failureMessage(message);
    state.$store.dispatch("set_state_after_logout");
    state.$router.push("/");
    return
}
export function logout(state) {
    state.$flashMessage.successMessage("Logged out");
    state.$store.dispatch("set_state_after_logout");
    state.$router.push("/");
    return
}
