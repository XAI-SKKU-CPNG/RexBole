/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
export const $RecommendationOut = {
    properties: {
        rec_item_id: {
            type: 'number',
            isRequired: true,
        },
        rec_item_name: {
            type: 'string',
            isRequired: true,
        },
        explanations: {
            type: 'array',
            contains: {
                type: 'ExplainationOut',
            },
            isRequired: true,
        },
    },
} as const;
