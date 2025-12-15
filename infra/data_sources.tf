data "aws_ssm_parameter" "jwt_secret" {
  name            = "jwt_secret"
  with_decryption = true
}
