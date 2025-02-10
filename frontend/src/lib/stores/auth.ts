import { writable } from 'svelte/store';

// A writable store to track edit permissions
export const canEdit = writable(false);
