#version 150

uniform sampler2D DiffuseSampler;
uniform sampler2D DiffuseDepthSampler;
uniform sampler2D TranslucentSampler;
uniform sampler2D TranslucentDepthSampler;
uniform sampler2D ItemEntitySampler;
uniform sampler2D ItemEntityDepthSampler;
uniform sampler2D ParticlesSampler;
uniform sampler2D ParticlesDepthSampler;
uniform sampler2D WeatherSampler;
uniform sampler2D WeatherDepthSampler;
uniform sampler2D CloudsSampler;
uniform sampler2D CloudsDepthSampler;

in vec2 texCoord;

#define NUM_LAYERS 6
#define HALF_PI 1.57079632679

vec4 converge_color = vec4(0.0625,0.15625,0.21875,1.0) * 1.5;

vec4 color_layers[NUM_LAYERS];
float depth_layers[NUM_LAYERS];
int active_layers = 0;

out vec4 fragColor;

float calc_converge_rate(float depth) {
    if (depth == 1.0){
        return 0.0;
    } else {
        return pow(max((1.0 - (1.0 - depth) * 50),0.0),7);
    }
}

void try_insert( vec4 color, float depth, bool converge) {
    if ( color.a == 0.0 ) {
        return;
    }

    if (converge) {
        float converge_rate = calc_converge_rate(depth);
        color_layers[active_layers] = vec4( (color * (1 - converge_rate) + converge_color * converge_rate).rgb ,color.a );
    } else {
        color_layers[active_layers] = color;
    }


    depth_layers[active_layers] = depth;

    int jj = active_layers++;
    int ii = jj - 1;
    while ( jj > 0 && depth_layers[jj] > depth_layers[ii] ) {
        float depthTemp = depth_layers[ii];
        depth_layers[ii] = depth_layers[jj];
        depth_layers[jj] = depthTemp;

        vec4 colorTemp = color_layers[ii];
        color_layers[ii] = color_layers[jj];
        color_layers[jj] = colorTemp;

        jj = ii--;
    }
}

vec3 blend( vec3 dst, vec4 src ) {
    return ( dst * ( 1.0 - src.a ) ) + src.rgb;
}

void main() {
    active_layers = 0;

    try_insert(vec4( texture( DiffuseSampler, texCoord ).rgb, 1.0 ), texture( DiffuseDepthSampler, texCoord ).r ,true);
    try_insert( texture( TranslucentSampler, texCoord ), texture( TranslucentDepthSampler, texCoord ).r ,true);
    try_insert( texture( ItemEntitySampler, texCoord ), texture( ItemEntityDepthSampler, texCoord ).r ,true);
    try_insert( texture( ParticlesSampler, texCoord ), texture( ParticlesDepthSampler, texCoord ).r ,true);
    try_insert( texture( WeatherSampler, texCoord ), texture( WeatherDepthSampler, texCoord ).r ,false);
    try_insert( texture( CloudsSampler, texCoord ), texture( CloudsDepthSampler, texCoord ).r ,false);

    vec3 texelAccum = color_layers[0].rgb;
    for ( int ii = 1; ii < active_layers; ++ii ) {
        texelAccum = blend( texelAccum, color_layers[ii] );
    }

    fragColor = sin(vec4( texelAccum.rgb, 1.0 ) * HALF_PI);
}
