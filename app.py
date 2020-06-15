from phyber_math import vec2, vec4, mat4x4

identity = mat4x4.make_identity()
identity2 = mat4x4.make_identity()

identity = mat4x4.mat_mat_multiply(identity, identity2)

print(identity)

identity = identity * 2
v1 = vec4(20, 6, 54, -90)

print(identity * v1)
