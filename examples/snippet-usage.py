#! /usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2014, Nicolas P. Rougier. All Rights Reserved.
# Distributed under the (new) BSD License.
# -----------------------------------------------------------------------------
from glumpy import gloo

transform_1 = gloo.Snippet("""
uniform float scale;
float forward(float x) { return scale*x; }
float inverse(float x) { return scale*x; }
""")

transform_2 = gloo.Snippet("""
uniform float scale;
float forward(float x) { return x*scale; }
float inverse(float x) { return x*scale; }
""")

transform_3 = gloo.Snippet("""
vec2 compose(float x, float y) { return vec2(x,y); }
vec2 compose(vec2 xy) { return xy; }
""")

code= """
void main(void)
{
    // ---

    float scale = <transform_1.scale>;
    float scale = <transform_2.scale>;


    // ---

    // Argument must be given through snippet
    <transform_1>;

    // Argument cannot be given through snippet
    <transform_2>(B);

    // Argument can be overriden throught snippet
    <transform_3(C)>;

    // ---

    // Default function (first defined) is used
    <transform_4>;

    // Forward function is used
    <transform_5.forward>;

    // Inverse function is used
    <transform_6.inverse>;

    // ---

    // Compose snippet with speficif field affectation
    <transform_7>;

    // Compose snippet with generic field affectation
    // Note yet done
    // <transform_8(H)>;

} """

program = gloo.Program(code,"void main(){}")
program["transform_1"] = transform_1("A")
program["transform_2"] = "forward"
program["transform_3"] = transform_1()
program["transform_4"] = transform_1("D")
program["transform_5"] = transform_2("E")
program["transform_6"] = transform_2("F")
program["transform_7"] = transform_3(transform_1("G.x"), transform_2("G.y"))
#program["transform_8"] = transform_3( ('x',transform_1()), ('y',transform_2()) )
print program.vertex.code


# Make sure that if snippet code has been already included in another program
# it is nonetheless included in the new program
code= """
void main(void)
{
    // Argument must be given through snippet
    <transform>;
"""
program = gloo.Program(code,"void main(){}")
program["transform"] = transform_1("A")
print program.vertex.code