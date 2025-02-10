<script>
	import Header from "./Header.svelte";
	import "../app.css";
	import 'bootstrap-icons/font/bootstrap-icons.css';
	import 'bootstrap/dist/css/bootstrap.min.css';
</script>

<div class="app">
	<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css" />

	<Header />

	<main>
		<slot />
	</main>

	<footer>
		<a href={'https://www.datascience.ch/'}>
			<img src='/logos/sdsc_white.svg' width={206} height={33} alt='logo-footer' />
		</a>
	</footer>
</div>

<style>
	
	.app {
		display: flex;
		flex-direction: column;
		min-height: 100vh;
	}

	main {
		flex: 1;
		display: flex;
		flex-direction: column;
		padding: 1rem;
		width: 100%;
		max-width: 80rem;
		margin: 0 auto;
		box-sizing: border-box;
	}

	footer {
		display: flex;
		flex-direction: row;
		justify-content: end;
		align-items: end;
		padding: 22px;
		background-color: var(--primary-dark-color);
	}

	footer a {
		font-weight: bold;
	}

	@media (min-width: 480px) {
		footer {
			padding: 12px 0;
		}
	}

</style>
